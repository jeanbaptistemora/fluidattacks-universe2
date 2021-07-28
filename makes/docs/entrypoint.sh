# shellcheck shell=bash

function main {
  local src='docs/src'
  export env='prod'

  pushd "${src}" \
    && rm -rf node_modules \
    && copy "__argNodeModules__" node_modules \
    && npm run "${@}" \
    && popd \
    || return 1
}

main "${@}"
