# shellcheck shell=bash

function main {
  : && pushd integrates/front \
    && copy __argSetupIntegratesFrontDevRuntime__ ./node_modules \
    && tsc -p tsconfig.json \
    && lint_typescript . . \
    && popd \
    || return 1
}

main "$@"
