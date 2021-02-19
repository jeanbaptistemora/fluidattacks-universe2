# shellcheck shell=bash

function main {

      copy "${envSrcIntegratesMobile}" "${out}" \
  &&  copy "${envSetupIntegratesMobileDevRuntime}/node_modules" "${out}/node_modules" \
  &&  chmod 755 "${out}/node_modules/.bin/tsc" "${out}/node_modules/.bin/tslint" \
  &&  pushd "${out}" \
    &&  npm run lint \
  &&  popd \
  ||  return 1
}

main "${@}"
