# shellcheck shell=bash

source "${envBashLibCommon}"

function setup_integrates_mobile_runtime {
      mkdir -p "${out}/node_modules" \
  &&  copy "${envNodeRequirements}/node_modules" "${out}/node_modules"
}

setup_integrates_mobile_runtime
