# shellcheck shell=bash

function main {
  local src='makes/applications/makes/doc/src'
  export env='prod'

      pushd "${src}" \
    &&  copy "__envRuntime__/node_modules" node_modules \
    &&  chmod +x node_modules/.bin/* \
    &&  npm run "${@}" \
    &&  rm -rf node_modules \
  &&  popd \
  ||  return 1
}

main "${@}"
