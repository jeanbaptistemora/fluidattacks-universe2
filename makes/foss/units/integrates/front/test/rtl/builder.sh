# shellcheck shell=bash

function main {
  copy "${envSrcIntegratesFront}" "${out}" \
    && copy "${envSetupIntegratesFrontDevRuntime}" "${out}/node_modules" \
    && pushd "${out}" \
    && npm run test:rtl \
    && popd \
    || return 1
}

main "${@}"
