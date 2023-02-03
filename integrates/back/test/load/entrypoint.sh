# shellcheck shell=bash

function main {
  : \
    && pushd integrates/back/test/load \
    && rm -rf node_modules \
    && copy __argRuntime__ node_modules \
    && npm run test \
    && popd \
    || return 1
}

main "${@}"
