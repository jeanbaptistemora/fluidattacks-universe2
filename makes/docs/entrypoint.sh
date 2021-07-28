# shellcheck shell=bash

function _clean {
  local src="${1}"
  local node_modules="${src}/node_modules"
  local vulns="${src}/docs/criteria2/vulnerabilities"
  local vulns_regex="[0-9]{3}\.md"

  rm -rf "${node_modules}" \
    && find "${vulns}" -name "${vulns_regex}" -delete
}

function main {
  local src='docs/src'
  local action="${1}"
  export env="${2:-prod}"
  export branch="${3:-default}"

  _clean "${src}" \
    && generate-criteria \
    && pushd "${src}" \
    && copy "__argNodeModules__" node_modules \
    && npm run "${action}" \
    && popd \
    || return 1
}

main "${@}"
