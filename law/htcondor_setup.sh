#!/usr/bin/env bash

action() {

    local shell_is_zsh="$( [ -z "${ZSH_VERSION}" ] && echo "false" || echo "true" )"
    local finalfits_setup_file="$( ${shell_is_zsh} && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    local finalfits_script_dir="$( cd "$( dirname "${finalfits_setup_file}" )" && pwd )"
    local finalfits_analysis_dir="$( cd "${finalfits_script_dir}/.." && pwd )"

    cd "${finalfits_analysis_dir}" || return 1
    export ANALYSIS_PATH="${finalfits_analysis_dir}"
    # The following source of cmsset_default.sh is needed on architectures other than lxplus, when the default cms commands are not sourced at startup
    export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
    source $VO_CMS_SW_DIR/cmsset_default.sh
    cmsenv
    local finalfits_install_dir="${finalfits_analysis_dir}/law/install_dir"
    local finalfits_shared_install_dir="$( dirname "${finalfits_analysis_dir}" )/flashggFinalFit/law/install_dir"
    if [ ! -d "${finalfits_install_dir}" ] || [ -z "$(ls -A "${finalfits_install_dir}" 2>/dev/null)" ]; then
        if [ -d "${finalfits_shared_install_dir}" ] && [ -n "$(ls -A "${finalfits_shared_install_dir}" 2>/dev/null)" ]; then
            finalfits_install_dir="${finalfits_shared_install_dir}"
            echo "Using shared law installation at ${finalfits_install_dir}"
        else
            PYTHONUSERBASE="${finalfits_install_dir}" pip3 install --user --no-cache-dir --force-reinstall "git+https://github.com/riga/law.git@master"
        fi
    else
        echo "Directory ${finalfits_install_dir} already exists and is not empty. Using local law installation..."
    fi

    export INSTALL_DIR="${finalfits_install_dir}"
    export PYTHONPATH="${PYTHONPATH}:${INSTALL_DIR}/lib/python3.9/site-packages"
    export PATH="${INSTALL_DIR}/bin:${PATH}"

    export PYTHONPATH="${finalfits_analysis_dir}:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Background:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Trees2WS:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Trees2WS/T2WSTools:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Signal:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Signal/tools:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/commonTools:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Datacard:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Datacard/datacardTools:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Combine:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Plots/Spectra:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/Plots/Spectra/fidXS:${PYTHONPATH}"
    export PYTHONPATH="${finalfits_analysis_dir}/law/:${PYTHONPATH}"
    export LAW_HOME="${finalfits_analysis_dir}/law/.law"
    export LAW_CONFIG_FILE="${finalfits_analysis_dir}/law/law.cfg"
    export LAW_DIR="${finalfits_analysis_dir}/law"

    source "$( law completion )" ""
}
action
