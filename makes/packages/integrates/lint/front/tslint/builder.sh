# shellcheck shell=bash

source "${envBashLibCommon}"
source "${envSearchPaths}"

function main {

      copy "${envSrcIntegratesFront}" "${out}" \
  &&  copy "${envSetupIntegratesDevelopmentFront}/node_modules" "${out}/node_modules" \
  &&  copy "${envSetupIntegratesRuntimeFront}/node_modules" "${out}/node_modules" \
  &&  chmod 755 -R "${out}/node_modules" \
  &&  pushd "${out}" \
    &&  npm run lint:tslint \
  &&  popd \
  ||  return 1
}

main "$@"
