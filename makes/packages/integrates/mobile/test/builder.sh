# shellcheck shell=bash

source "${envBashLibCommon}"
source "${envSearchPaths}"

function main {
      copy "${envSrcIntegratesMobile}" "${out}" \
  &&  copy "${envSetupIntegratesMobileDevRuntime}/node_modules" "${out}/node_modules" \
  &&  chmod 755 "${out}/node_modules/.bin/jest" \
  &&  pushd "${out}" \
    &&  npm test \
  &&  popd \
  ||  return 1
}

main "${@}"
