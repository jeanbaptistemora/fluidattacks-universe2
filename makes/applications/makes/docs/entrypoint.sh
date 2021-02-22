# shellcheck shell=bash

function main {
  local src='makes/applications/makes/docs/src'

      pushd "${src}" \
    &&  copy "__envRuntime__/node_modules" node_modules \
    &&  chmod -R 775 node_modules \
    &&  npm run "${@}" \
    &&  rm -rf node_modules \
  &&  popd \
  || return 1
}

main "${@}"
