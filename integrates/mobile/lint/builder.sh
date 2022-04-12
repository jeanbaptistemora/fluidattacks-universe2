# shellcheck shell=bash

function main {

  copy "${envSrcIntegratesMobile}" "${out}" \
    && copy "${envSetupIntegratesMobileDevRuntime}" "${out}/node_modules" \
    && pushd "${out}" \
    && lint_typescript "$(pwd)" "$(pwd)" \
    && popd \
    || return 1
}

main "${@}"
