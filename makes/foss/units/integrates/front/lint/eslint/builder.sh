# shellcheck shell=bash

function main {
  copy "${envSrcIntegratesFront}" "${out}" \
    && copy "${envSetupIntegratesFrontDevRuntime}" "${out}/node_modules" \
    && pushd "${out}" \
    && tcm src/ --silent \
    && tsc -p tsconfig.json \
    && lint_typescript "${out}" "${out}" \
    && popd \
    || return 1
}

main "$@"
