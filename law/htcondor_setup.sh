#!/usr/bin/env bash

action() {

    local shell_is_zsh="$( [ -z "${ZSH_VERSION}" ] && echo "false" || echo "true" )"
    local this_file="$( ${shell_is_zsh} && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    local script_dir="$( cd "$( dirname "${this_file}" )" && pwd )"
    local this_dir="$( cd "${script_dir}/.." && pwd )"

    cd "${this_dir}" || return 1
    export ANALYSIS_PATH="${this_dir}"
    # The following source of cmsset_default.sh is needed on architectures other than lxplus, when the default cms commands are not sourced at startup
    export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
    source $VO_CMS_SW_DIR/cmsset_default.sh
    cmsenv
    local install_dir="${this_dir}/law/install_dir"
    local shared_install_dir="$( dirname "${this_dir}" )/flashggFinalFit/law/install_dir"
    if [ ! -d "${install_dir}" ] || [ -z "$(ls -A "${install_dir}" 2>/dev/null)" ]; then
        if [ -d "${shared_install_dir}" ] && [ -n "$(ls -A "${shared_install_dir}" 2>/dev/null)" ]; then
            install_dir="${shared_install_dir}"
            echo "Using shared law installation at ${install_dir}"
        else
            PYTHONUSERBASE="${install_dir}" pip3 install --user --no-cache-dir --force-reinstall "git+https://github.com/riga/law.git@master"
        fi
    else
        echo "Directory ${install_dir} already exists and is not empty. Using local law installation..."
    fi

    export INSTALL_DIR="${install_dir}"
    export PYTHONPATH="${PYTHONPATH}:${INSTALL_DIR}/lib/python3.9/site-packages"
    export PATH="${INSTALL_DIR}/bin:${PATH}"

    export PYTHONPATH="${this_dir}:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Background:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Trees2WS:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Trees2WS/T2WSTools:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Signal:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Signal/tools:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/commonTools:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Datacard:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Datacard/datacardTools:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Combine:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Plots/Spectra:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/Plots/Spectra/fidXS:${PYTHONPATH}"
    export PYTHONPATH="${this_dir}/law/:${PYTHONPATH}"
    export LAW_HOME="${this_dir}/law/.law"
    export LAW_CONFIG_FILE="${this_dir}/law/law.cfg"
    export LAW_DIR="${this_dir}/law"

    source "$( law completion )" ""
}
action
