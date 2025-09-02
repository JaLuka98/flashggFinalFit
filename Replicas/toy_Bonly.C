#include <filesystem>
#include <sstream>
#include <vector>
namespace fs = std::filesystem;

std::string getDataHistName(const std::string& filename, bool inclusive_file) {
    if (inclusive_file) {
        // Since there is no RECO in the filename..
        size_t catPos = filename.find("_cat");
        if (catPos == std::string::npos) return "";

        // Find the start of the category
        size_t catStart = catPos + 4; // length of "_cat"
        // Find the end (before ".root")
        size_t rootPos = filename.rfind(".root");
        if (rootPos == std::string::npos || rootPos <= catStart) return "";

        std::string cat = filename.substr(catStart, rootPos - catStart);
        return "roohist_data_mass_cat" + cat;
    }
    else {
        // Find "RECO_" in the filename
        size_t recoPos = filename.find("RECO_");
        if (recoPos == std::string::npos) return "";

        // Find the start of the category
        size_t catStart = recoPos + 5; // length of "RECO_"
        // Find the end (before ".root")
        size_t rootPos = filename.rfind(".root");
        if (rootPos == std::string::npos || rootPos <= catStart) return "";

        std::string cat = filename.substr(catStart, rootPos - catStart);
        return "roohist_data_mass_RECO_" + cat;
    }

}

// Hilfsfunktion zum Parsen des Eingabestrings
std::vector<std::pair<std::string, int>> parsePdfIndices(const std::string& input) {
    std::vector<std::pair<std::string, int>> result;
    std::stringstream ss(input);
    std::string item;
    while (std::getline(ss, item, ',')) {
        size_t eqPos = item.find('=');
        if (eqPos != std::string::npos) {
            std::string name = item.substr(0, eqPos);
            int value = std::stoi(item.substr(eqPos + 1));
            result.emplace_back(name, value);
        }
    }
    return result;
}

// Hilfsfunktion zum Extrahieren des Kategorienamens
std::string getCategoryName(const std::string& filename) {
    size_t start = filename.find("CMS-HGG_multipdf_");
    if (start == std::string::npos) return "";
    start += strlen("CMS-HGG_multipdf_");
    size_t end = filename.rfind(".root");
    if (end == std::string::npos || end <= start) return "";
    return filename.substr(start, end - start);
}

void toy_Bonly(const char* inputFolder, const char* outputFile, const char* pdfindex, int seed) {
    std::vector<std::string> rootFiles;
    for (const auto& entry : fs::directory_iterator(inputFolder)) {
        if (entry.path().extension() == ".root") {
            rootFiles.push_back(entry.path());
        }
    }
    std::sort(rootFiles.begin(), rootFiles.end());

    // pdfindices setzen und fixieren
    std::vector<std::pair<std::string, int>> indices;
    std::string indices_str = pdfindex;
    if (!indices_str.empty()) {
        indices = parsePdfIndices(indices_str);
        // std::cout << "Indices: " << indices << std::endl;
        std::cout << "Indices:" << std::endl;
        for (const auto& [name, val] : indices) {
            std::cout << "  " << name << " = " << val << std::endl;
        }
    }
    if (indices.empty()) {
        std::cerr << "Error: No valid pdfindex provided." << std::endl;
        return;
    }

    RooDataSet* mergedToy = nullptr;
    RooArgSet* vars = nullptr;
    RooCategory CMS_channel("CMS_channel", "Channel name");

    // ...vor dem Event-Loop...
    std::vector<std::string> catNames;
    for (const auto& filename : rootFiles) {
        catNames.push_back(getCategoryName(filename));
    }
    for (size_t i = 0; i < catNames.size(); ++i) {
        CMS_channel.defineType(catNames[i].c_str(), i);
    }

    for (size_t fileIdx = 0; fileIdx < rootFiles.size(); ++fileIdx) {
        const auto& filename = rootFiles[fileIdx];
        TFile* file = TFile::Open(filename.c_str());
        if (!file || file->IsZombie()) continue;

        // Kategorie-Label aus Dateiname extrahieren und in RooCategory definieren
        std::string catName = catNames[fileIdx];
        std::cout << "Category name: " << catName << std::endl;

        // Initialisiere bestFit_idx für jede Kategorie
        int bestFit_idx = -1;

        for (const auto& [name, val] : indices) {
            // std::cout << "Checking index: " << name << " = " << catName << std::endl;
            if (name.find(catName) != std::string::npos) {
                bestFit_idx = val;
                break;  // stop once we find it
            }
        }

        std::cout << "Best fit index for category " << catName << ": " << bestFit_idx << std::endl;

        RooWorkspace* ws = (RooWorkspace*)file->Get("multipdf");
        if (!ws) { file->Close(); continue; }

        RooRealVar* obs = ws->var("CMS_hgg_mass");
        obs->setBins(320);
        if (!obs) { file->Close(); continue; }

        RooMultiPdf* multipdf = nullptr;
        const RooArgSet pdfs = ws->allPdfs();
        TIterator* pdfIt = pdfs.createIterator();
        TObject* pdfObj;
        while ((pdfObj = (TObject*)pdfIt->Next())) {
            if (pdfObj->InheritsFrom("RooMultiPdf")) {
                multipdf = (RooMultiPdf*)pdfObj;
                break;
            }
        }
        delete pdfIt;
        if (!multipdf) { file->Close(); continue; }

        RooAbsPdf* pdf = multipdf->getPdf(bestFit_idx);

        bool inclusive_file = (catName == "cat0" || catName == "cat1" || catName == "cat2");

        std::string dataHistName = getDataHistName(filename, inclusive_file);
        RooAbsData* data = ws->data(dataHistName.c_str());
        if (!data) { file->Close(); continue; }

        RooRealVar* n_yield = new RooRealVar("n_yield", "Fitted yield", 1000, 0, 1e6);
        RooExtendPdf* extPdf = new RooExtendPdf("extPdf", "extended pdf", *pdf, *n_yield);

        extPdf->fitTo(*data,
            RooFit::Extended(),
            RooFit::PrintLevel(-1));

        double fitted_yield = n_yield->getVal();

        int catSeed = seed + 1000000 * fileIdx; // Großer Offset, um Überschneidungen zu vermeiden
        TRandom3 *rng = new TRandom3(catSeed); // Setze den Seed für die Zufallszahlengenerierung für den Poissonian
        int nToys = rng->Poisson(fitted_yield);

        RooArgSet genVars(*obs); // Nur über obs generieren!
        RooRandom::randomGenerator()->SetSeed(catSeed); // Setze nochmal den Seed für die Zufallszahlengenerierung für RooFit. Duh...
        RooDataSet* toyData = pdf->generate(genVars, nToys);

        CMS_channel.setLabel(catName.c_str()); // Setze Wert für diese Kategorie
        cout << "Processing category: " << catName << " (channel_number=" << fileIdx << ")" << std::endl;

        if (!vars) {
            RooArgSet tmpVars(*obs, CMS_channel);
            vars = (RooArgSet*)tmpVars.snapshot();
        }
        if (!mergedToy) {
            mergedToy = new RooDataSet("toy_1", "All toys", *vars);
        }
        for (int i = 0; i < toyData->numEntries(); ++i) {
            RooArgSet entry(*toyData->get(i));
            entry.add(CMS_channel); // Füge die Variable mit richtigem Wert hinzu
            mergedToy->add(entry);
        }

        delete toyData;
        delete extPdf;
        delete n_yield;
        file->Close();
    }

    TFile* output_file = TFile::Open(outputFile, "RECREATE");
    output_file->mkdir("toys");
    output_file->cd("toys");
    if (mergedToy) {
        mergedToy->SetName("toy_1");
        mergedToy->Write();
    }
    output_file->Close();
    delete mergedToy;
}