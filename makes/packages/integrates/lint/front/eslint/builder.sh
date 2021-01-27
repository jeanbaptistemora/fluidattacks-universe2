# shellcheck shell=bash

source "${envBashLibCommon}"
source "${envSetupIntegratesDevelopmentFront}"
source "${envSetupIntegratesRuntimeFront}"

function main {

      copy "${envSrcIntegratesFront}" "${out}" \
  &&  pushd "${out}" \
    &&  npm run lint:eslint \
  &&  popd \
  ||  return 1
}

main "$@"
