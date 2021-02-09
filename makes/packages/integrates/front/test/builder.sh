# shellcheck shell=bash

source "${envBashLibCommon}"
source "${envSearchPaths}"

function main {

      copy "${envSrcIntegratesFront}" "${out}" \
  &&  copy "${envSetupIntegratesFrontDevRuntime}/node_modules" "${out}/node_modules" \
  &&  chmod 755 "${out}/node_modules/.bin/tcm" "${out}/node_modules/.bin/jest" \
  &&  pushd "${out}" \
    &&  npm test \
  &&  popd \
  || return 1
}

main "${@}"
