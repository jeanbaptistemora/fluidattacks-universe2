# shellcheck shell=bash

function main {

  copy "${envSrcIntegratesMobile}" "${out}" \
    && copy "${envSetupIntegratesMobileDevRuntime}" "${out}/node_modules" \
    && pushd "${out}" \
    && npm run test:rtl \
    && popd \
    || return 1
}

main "${@}"
