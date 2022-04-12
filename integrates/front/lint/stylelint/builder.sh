# shellcheck shell=bash

function main {

  copy "${envSrcIntegratesFront}" "${out}" \
    && copy "${envSetupIntegratesFrontDevRuntime}" "${out}/node_modules" \
    && pushd "${out}" \
    && if stylelint '**/*.css' --output-file; then
      echo '[INFO] All styles are ok!'
    else
      err_count="$(stylelint '**/*.css' | wc -l || true)" \
        && echo "[ERROR] ${err_count} errors found in styles!" \
        && return 1
    fi \
    && popd \
    || return 1
}

main "$@"
