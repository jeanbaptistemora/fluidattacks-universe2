# shellcheck shell=bash

function main {
  local return_value=0

  : && pushd integrates/front \
    && copy __argSetupIntegratesFrontDevRuntime__ ./node_modules \
    && if stylelint '**/*.css' --output-file; then
      info 'All styles are ok!'
    else
      info 'Some files do not follow the suggested style.' \
        && info 'we will fix some of the issues automatically,' \
        && info 'but the job will fail.' \
        && { stylelint '**/*.css' --fix --output-file || true; } \
        && return_value=1
    fi \
    && popd \
    && return "${return_value}"
}

main "$@"
