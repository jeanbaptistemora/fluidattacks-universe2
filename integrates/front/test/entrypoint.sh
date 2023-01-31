# shellcheck shell=bash

function main {
  : \
    && pushd integrates/front \
    && rm -rf node_modules \
    && copy __argRuntime__ node_modules \
    && npm run test \
      -- \
      --shard "${CI_NODE_INDEX:-1}/${CI_NODE_TOTAL:-1}" \
    && popd \
    || return 1
}

main "${@}"
