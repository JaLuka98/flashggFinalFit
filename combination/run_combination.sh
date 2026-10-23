#!/bin/bash
# Hgg+H4l combination (2022+2023+2024, total-XS extrapolation): from the raw Hgg and H4l cards to the
# Hgg-only, H4l-only and Hgg+H4l fits. See combination/README.md for the full chain.
#
# Usage:  combination/run_combination.sh <obs> <step> [<step> ...]
#   obs:  inclusive PTH rapidity NJ PTJ0 MassJ0J1
#   steps (in this order):
#     hgg-card   raw Hgg card -> <raw>_total.txt next to it: acceptance rows (CMS_HIG25015_*_accMatrix,
#                2022+2023 inputs) + branching-ratio rows (HiggsDecayWidthTHU_*, param_alphaS, param_mq)
#     h4l-card   raw H4l floating-ZZ card -> <raw>_comb.txt next to it (BR_hzz* removed, per-era pileup
#                merged, BR rows); an existing _comb card must be reproduced exactly
#     cards      combineCards.py hgg= h4l=, then the hgg-only / h4l-only cards cut out with --ic
#                (CHANNELS=h4l: the H4l card alone)
#     t2w        POI map (Combine/makeCombinationMaps.py, verified on the combined card) + text2workspace
#     prepare    put cards and workspaces where law expects them
#     law        expected (Asimov) fits: law run FinalFitsYear --asimov-fits, for every fit in $FITS
#     unblind    observed fits: law run FinalFitsYear --unblinded-fits
#     summary    results tables (summarize_scans.py) and Hgg/H4l/comb comparison plots per POI
#
# Environment (defaults in brackets):
#   OUT       output folder [<repo>/output_combination_<obs>]
#   CHANNELS  "hgg h4l" (full combination) or "h4l" (H4l only, no Hgg card needed: the cards step builds
#             the H4l card alone, same content as the one cut out of the combined card) ["hgg h4l"]
#   FITS      fits to run ["hgg h4l comb", or "h4l" with CHANNELS=h4l]
#   HGG_CARD  raw Hgg card [differential: <repo>/output_2022_2023_2024_<obs>/Combine/Datacard_<obs>_2022_2023_2024.txt
#             (produced in this checkout by law run FinalFits, see README);
#             inclusive: $STAGE/Hyy_datacards_smoothed_decorrelation/raw/inclusive/Datacard_2022_2023_2024.txt]
#   STAGE     shared inputs [/net/data_cms3a-2/nobackup/group_JE_CMS/Hyy_Hzz_combination]
#   KIND      summary of asimov or dataFit [asimov]
#   FINALFITS_MH  [125.07]

set -eo pipefail

OBS=${1:?usage: $0 <obs> <step> [<step> ...]}
shift
[ $# -gt 0 ] || { sed -n 2,28p "${BASH_SOURCE[0]}"; exit 1; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "${HERE}/.." && pwd)"
CMSSW_SRC="$(cd "${REPO}/.." && pwd)"
STAGE=${STAGE:-/net/data_cms3a-2/nobackup/group_JE_CMS/Hyy_Hzz_combination}
OUT=${OUT:-${REPO}/output_combination_${OBS}}
CHANNELS=${CHANNELS:-"hgg h4l"}
case "${CHANNELS}" in
  "hgg h4l") FITS=${FITS:-"hgg h4l comb"} ;;
  h4l)       FITS=${FITS:-h4l} ;;
  *) echo "CHANNELS must be \"hgg h4l\" or h4l"; exit 1 ;;
esac
KIND=${KIND:-asimov}
export FINALFITS_MH=${FINALFITS_MH:-125.07}
YEAR=2022_2023_2024

# obs -> law variable | acceptance input folder | HiggsDNA observable label | H4l card variable
case "${OBS}" in
  inclusive) LAW_VAR="";         ACC_DIR=inclusive; ACC_OBS=PTH;      H4L_VAR=mass4l ;;
  PTH)       LAW_VAR=PTH;        ACC_DIR=PTH;       ACC_OBS=PTH;      H4L_VAR=pT4l ;;
  rapidity)  LAW_VAR=rapidity;   ACC_DIR=rapidity;  ACC_OBS=YH;       H4L_VAR=rapidity4l ;;
  NJ)        LAW_VAR=NJ;         ACC_DIR=NJ;        ACC_OBS=NJ;       H4L_VAR=Nj_2p5 ;;
  PTJ0)      LAW_VAR=PTJ0;       ACC_DIR=PTJ0;      ACC_OBS=PTJ0;     H4L_VAR=pTj1_2p5 ;;
  MassJ0J1)  LAW_VAR=MassJ0J1;   ACC_DIR=MassJ0J1;  ACC_OBS=MassJ0J1; H4L_VAR=mjj_4p7 ;;
  *) echo "unknown observable ${OBS}"; exit 1 ;;
esac

if [ -z "${HGG_CARD}" ]; then
  if [ "${OBS}" = inclusive ]; then
    HGG_CARD=${STAGE}/Hyy_datacards_smoothed_decorrelation/raw/inclusive/Datacard_${YEAR}.txt
  else
    HGG_CARD=${REPO}/output_${YEAR}_${OBS}/Combine/Datacard_${OBS}_${YEAR}.txt
  fi
fi
HGG_TOTAL=${HGG_CARD%.txt}_total.txt
H4L_RAW=${STAGE}/Hzz_datacards_floating_bkg/hzz4l_all_13TeV_xs_${H4L_VAR}_zzfloating_bin_v3.txt
H4L_COMB=${H4L_RAW%.txt}_comb.txt
ACC_INPUTS=${STAGE}/fiducial_samples/acceptance_2022_2023/${ACC_DIR}
if [ "${OBS}" = inclusive ]; then
  CARD_NAME=Datacard_${YEAR}; RUN_DIR=runFits_mu_fiducial
else
  CARD_NAME=Datacard_${OBS}_${YEAR}; RUN_DIR=runFits_${OBS}
fi

setup_cmssw() {
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  pushd "${CMSSW_SRC}" > /dev/null; eval "$(scramv1 runtime -sh)"; popd > /dev/null
  ulimit -s unlimited
}

card_of() { echo "${OUT}/cards/Datacard_${OBS}_$1.txt"; }
ws_of() { echo "${OUT}/workspaces/Datacard_${OBS}_$1.root"; }

do_hgg_card() {
  setup_cmssw
  [ -s "${HGG_CARD}" ] || { echo "raw Hgg card ${HGG_CARD} not found"; exit 1; }
  mkdir -p "${OUT}/logs"
  local acc="${OUT}/logs/hgg_card_with_acceptance.txt"
  python3 "${REPO}/Datacard/addAcceptanceUncertainties.py" --datacard "${HGG_CARD}" \
    --fidxs-dir "${ACC_INPUTS}" --obs "${ACC_OBS}" --output "${acc}"
  local fresh="${OUT}/logs/$(basename "${HGG_TOTAL}")"
  python3 "${REPO}/Datacard/addBranchingRatioUncertainties.py" --datacard "${acc}" --channel hgg \
    --mass "${FINALFITS_MH}" --output "${fresh}"
  rm -f "${acc}"
  # the card is written next to the raw card (relative shape paths); never overwrite a different one
  if [ -e "${HGG_TOTAL}" ]; then
    cmp -s "${fresh}" "${HGG_TOTAL}" || { echo "[ERROR] ${HGG_TOTAL} differs from a fresh preparation (${fresh})"; exit 1; }
    echo "Hgg card reproduced exactly: ${HGG_TOTAL}"
    rm -f "${fresh}"
  else
    mv "${fresh}" "${HGG_TOTAL}"
    echo "Hgg card for the combination: ${HGG_TOTAL}"
  fi
}

do_h4l_card() {
  setup_cmssw
  mkdir -p "${OUT}/logs"
  local fresh="${OUT}/logs/$(basename "${H4L_COMB}")"
  # prepareH4lCombinationCard writes next to its input; run it on a copy and compare
  cp -f "${H4L_RAW}" "${OUT}/logs/$(basename "${H4L_RAW}")"
  python3 "${REPO}/Datacard/prepareH4lCombinationCard.py" --datacard "${OUT}/logs/$(basename "${H4L_RAW}")" \
    --mass "${FINALFITS_MH}" --output "${fresh}"
  rm -f "${OUT}/logs/$(basename "${H4L_RAW}")"
  if [ -e "${H4L_COMB}" ]; then
    cmp -s "${fresh}" "${H4L_COMB}" || { echo "[ERROR] ${H4L_COMB} differs from a fresh preparation (${fresh})"; exit 1; }
    echo "H4l card reproduced exactly: ${H4L_COMB}"
    rm -f "${fresh}"
  else
    mv "${fresh}" "${H4L_COMB}"
    echo "H4l card for the combination: ${H4L_COMB}"
  fi
}

do_cards() {
  setup_cmssw
  [ "${CHANNELS}" = h4l ] && { do_cards_h4l; return; }
  [ -s "${HGG_TOTAL}" ] || { echo "run the hgg-card step first (${HGG_TOTAL} missing)"; exit 1; }
  [ -s "${H4L_COMB}" ] || { echo "run the h4l-card step first (${H4L_COMB} missing)"; exit 1; }
  mkdir -p "${OUT}/cards"
  cd "${OUT}/cards"
  combineCards.py hgg="${HGG_TOTAL}" h4l="${H4L_COMB}" > "$(card_of comb)"
  combineCards.py --ic='hgg_.*' "$(card_of comb)" > raw_hgg.txt
  combineCards.py --ic='h4l_.*' "$(card_of comb)" > raw_h4l.txt
  # drop nuisances that only act on the other channel (H4l signal-shape params in the Hgg card;
  # Hgg envelope indices and photon-shape params in the H4l card) and the ch1_ bin prefix
  python3 "${HERE}/clean_card.py" raw_hgg.txt "$(card_of hgg)" --drop '^CMS_HIG25015_zz4l_'
  python3 "${HERE}/clean_card.py" raw_h4l.txt "$(card_of h4l)" --drop '^(pdfindex_|CMS_HIG26007_)'
  rm raw_hgg.txt raw_h4l.txt
}

do_cards_h4l() {
  [ -s "${H4L_COMB}" ] || { echo "run the h4l-card step first (${H4L_COMB} missing)"; exit 1; }
  mkdir -p "${OUT}/cards"
  cd "${OUT}/cards"
  combineCards.py h4l="${H4L_COMB}" > raw_h4l.txt
  python3 "${HERE}/clean_card.py" raw_h4l.txt "$(card_of h4l)" --drop '^(pdfindex_|CMS_HIG26007_)'
  rm raw_h4l.txt
}

do_t2w() {
  setup_cmssw
  mkdir -p "${OUT}/workspaces" "${OUT}/logs"
  # map generated and verified on the combined card (every signal mapped once, no background);
  # the same model is used for the single-channel cards
  local map_card=comb
  [ "${CHANNELS}" = h4l ] && map_card=h4l
  python3 "${REPO}/Combine/makeCombinationMaps.py" --card "$(card_of ${map_card})" --obs "${OBS}" \
    --channels "${CHANNELS// /,}" --mass "${FINALFITS_MH}" --output "${OUT}/logs/t2w_map.sh" | tee "${OUT}/logs/map_check.log"
  local model
  model="$(sed -n '/-P HiggsAnalysis/,$p' "${OUT}/logs/t2w_map.sh" | tr -d '\\\n')"
  for fit in ${FITS}; do
    echo "text2workspace.py $(card_of ${fit}) -o $(ws_of ${fit}) -m ${FINALFITS_MH} ${model}" > "${OUT}/logs/t2w_${fit}.cmd"
    eval "text2workspace.py $(card_of ${fit}) -o $(ws_of ${fit}) -m ${FINALFITS_MH} ${model}" \
      > "${OUT}/logs/t2w_${fit}.log" 2>&1 &
  done
  wait
  for fit in ${FITS}; do
    [ -s "$(ws_of ${fit})" ] || { echo "text2workspace failed for ${fit}, see ${OUT}/logs/t2w_${fit}.log"; exit 1; }
  done
}

# law expects <output_dir>/Combine/Datacard[_<variable>]_<year>.{txt,root}
do_prepare() {
  for fit in ${FITS}; do
    mkdir -p "${OUT}/${fit}/Combine"
    ln -sfn "$(card_of ${fit})" "${OUT}/${fit}/Combine/${CARD_NAME}.txt"
    cp -f "$(ws_of ${fit})" "${OUT}/${fit}/Combine/${CARD_NAME}.root"
  done
}

run_law() {  # $1 = law flag (--asimov-fits / --unblinded-fits), $2 = log tag
  cd "${REPO}"
  # shellcheck disable=SC1091
  source law/htcondor_setup.sh
  cd "${REPO}/law"
  local var_opt=""
  [ -n "${LAW_VAR}" ] && var_opt="--variable ${LAW_VAR}"
  mkdir -p "${OUT}/logs"
  for fit in ${FITS}; do
    # shellcheck disable=SC2086
    setsid nohup law run FinalFitsYear --year ${YEAR} ${var_opt} $1 True \
      --output-dir "${OUT}/${fit}" --batch-system htcondor --batch-flavor htcondor --workers 4 \
      > "${OUT}/logs/law_$2_${fit}.log" 2>&1 < /dev/null &
    echo "${fit}: law running (pid $!), log: ${OUT}/logs/law_$2_${fit}.log"
  done
}

do_summary() {
  setup_cmssw
  python3 "${HERE}/summarize_scans.py" --base "${OUT}" --obs "${OBS}" --kind "${KIND}" --fits "${FITS}" --mass "${FINALFITS_MH}"
  mkdir -p "${OUT}/plots"
  local pois tag
  pois=$(python3 -c "import importlib.util as u; s=u.spec_from_file_location('m','${REPO}/Combine/makeCombinationMaps.py'); m=u.module_from_spec(s); s.loader.exec_module(m); print(' '.join(m.patterns('${OBS}')[1]))")
  [ "${KIND}" = asimov ] && tag=Asimov || tag=Data
  for poi in ${pois}; do
    scan() {
      if [ "${KIND}" = asimov ]; then echo "${OUT}/$1/Combine/${RUN_DIR}/asimov/higgsCombineAsimovPostFitScanFit_${poi}.root"
      else echo "${OUT}/$1/Combine/${RUN_DIR}/dataFit/higgsCombineDataPostFitScanFit_${poi}.MultiDimFit.mH${FINALFITS_MH}.root"; fi
    }
    # plot1DScan.py writes to "./<-o>", so run it inside the plot folder with a relative name
    local main=(comb "H#gamma#gamma+H4l") others=()
    [ "${CHANNELS}" = h4l ] && main=(h4l H4l) || others=(--others "$(scan hgg):H#gamma#gamma:4" "$(scan h4l):H4l:2")
    (cd "${OUT}/plots" && python3 "${CMSSW_SRC}/CombineHarvester/CombineTools/scripts/plot1DScan.py" \
      "$(scan ${main[0]})" --POI "${poi}" --main-label "${main[1]}" "${others[@]}" \
      -o "compare_${tag}_${poi}" > "${OUT}/logs/plot_compare_${tag}_${poi}.log" 2>&1) || \
      echo "comparison plot failed for ${poi}, see ${OUT}/logs/plot_compare_${tag}_${poi}.log"
  done
}

for step in "$@"; do
  case "${step}" in
    hgg-card) do_hgg_card ;;
    h4l-card) do_h4l_card ;;
    cards) do_cards ;;
    t2w) do_t2w ;;
    prepare) do_prepare ;;
    law) run_law --asimov-fits asimov ;;
    unblind) run_law --unblinded-fits unblind ;;
    summary) do_summary ;;
    *) echo "unknown step ${step}"; exit 1 ;;
  esac
done
