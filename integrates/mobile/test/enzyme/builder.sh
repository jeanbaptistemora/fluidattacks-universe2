# shellcheck shell=bash

function main {

  copy "${envSrcIntegratesMobile}" "${out}" \
    && copy "${envSetupIntegratesMobileDevRuntime}" "${out}/node_modules" \
    && pushd "${out}" \
    && npm run test:enzyme \
    && popd \
    || return 1
}

main "${@}"
