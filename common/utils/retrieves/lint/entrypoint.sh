# shellcheck shell=bash

function main {
  : && pushd common/utils/retrieves \
    && copy __argSetupRetrievesDevRuntime__ ./node_modules \
    && eslint . --ext ".ts" --fix \
    && popd \
    || return 1
}

main "$@"
