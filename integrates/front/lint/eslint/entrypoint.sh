# shellcheck shell=bash

function main {
  : && pushd integrates/front \
    && copy __argSetupIntegratesFrontDevRuntime__ ./node_modules \
    && tcm src/ --silent \
    && tsc -p tsconfig.json \
    && lint_typescript . . \
    && popd \
    || return 1
}

main "$@"
