# shellcheck shell=bash

source "${envBashLibCommon}"
source "${envSearchPaths}"

function main {

      copy "${envSrcIntegratesFront}" "${out}" \
  &&  copy "${envSetupIntegratesDevelopmentFront}/node_modules" "${out}/node_modules" \
  &&  copy "${envSetupIntegratesRuntimeFront}/node_modules" "${out}/node_modules" \
  &&  chmod -R 755 "${out}/node_modules" \
  &&  pushd "${out}" \
    &&  npm test \
  &&  popd \
  || return 1
}

main "${@}"
