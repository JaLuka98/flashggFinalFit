#include <filesystem>
namespace fs = std::filesystem;

std::string getDataHistName(const std::string& filename) {
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

// Hilfsfunktion zum Extrahieren des Kategorienamens
std::string getCategoryName(const std::string& filename) {
    size_t start = filename.find("CMS-HGG_multipdf_");
    if (start == std::string::npos) return "";
    start += strlen("CMS-HGG_multipdf_");
    size_t end = filename.rfind(".root");
    if (end == std::string::npos || end <= start) return "";
    return filename.substr(start, end - start);
}

void toy_Bonly(const char* inputFolder, const char* outputFile, int seed) {
    std::vector<std::string> rootFiles;
    for (const auto& entry : fs::directory_iterator(inputFolder)) {
        if (entry.path().extension() == ".root") {
            rootFiles.push_back(entry.path());
        }
    }
    std::sort(rootFiles.begin(), rootFiles.end());

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

        RooWorkspace* ws = (RooWorkspace*)file->Get("multipdf");
        if (!ws) { file->Close(); continue; }

        RooRealVar* obs = ws->var("CMS_hgg_mass");
        obs->setBins(80);
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

        RooAbsPdf* pdf = multipdf->getCurrentPdf();

        std::string dataHistName = getDataHistName(filename);
        RooAbsData* data = ws->data(dataHistName.c_str());
        if (!data) { file->Close(); continue; }

        RooRealVar* n_yield = new RooRealVar("n_yield", "Fitted yield", 1000, 0, 1e6);
        RooExtendPdf* extPdf = new RooExtendPdf("extPdf", "extended pdf", *pdf, *n_yield);

        extPdf->fitTo(*data, RooFit::Extended(), RooFit::PrintLevel(-1));
        double fitted_yield = n_yield->getVal();

        TRandom3 *rng = new TRandom3(seed);
        int nToys = rng->Poisson(fitted_yield);

        RooArgSet genVars(*obs); // Nur über obs generieren!
        RooDataSet* toyData = pdf->generate(genVars, nToys);

        // Kategorie-Label aus Dateiname extrahieren und in RooCategory definieren
        std::string catName = catNames[fileIdx];
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