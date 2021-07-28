# shellcheck shell=bash

function main {
  local src='docs/src'
  local to_clean=(
    "${src}/node_modules"
    "${src}/docs/criteria2/vulnerabilities"
  )
  export env='prod'

  rm -rf "${to_clean[@]}" \
    && generate-criteria-vulns \
    && pushd "${src}" \
    && copy "__argNodeModules__" node_modules \
    && npm run "${@}" \
    && popd \
    || return 1
}

main "${@}"
