# shellcheck shell=bash

function main {
  : && pushd common/utils/retrives \
    && copy __argSetupRetrievesDevRuntime__ ./node_modules \
    && tsc -p tsconfig.json \
    && eslint src/** --ext ".ts" \
    && popd \
    || return 1
}

main "$@"
