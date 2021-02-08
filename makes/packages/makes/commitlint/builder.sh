# shellcheck shell=bash

source "${envBashLibCommon}"

function setup_commitlint_runtime {
      mkdir -p "${out}/node_modules" \
  &&  copy "${envNodeRequirements}/node_modules" "${out}/node_modules"
}

setup_commitlint_runtime
