# shellcheck shell=bash

function main {

      copy "${envSrcIntegratesMobile}" "${out}" \
  &&  copy "${envSetupIntegratesMobileDevRuntime}/node_modules" "${out}/node_modules" \
  &&  pushd "${out}" \
    &&  npm run lint \
  &&  popd \
  ||  return 1
}

main "${@}"
