# shellcheck shell=bash

function main {

      copy "${envSrcIntegratesFront}" "${out}" \
  &&  copy "${envSetupIntegratesFrontDevRuntime}/node_modules" "${out}/node_modules" \
  &&  chmod 755 "${out}/node_modules/.bin/tcm" "${out}/node_modules/.bin/tsc" "${out}/node_modules/.bin/tslint" \
  &&  pushd "${out}" \
    &&  npm run lint:tslint \
  &&  popd \
  ||  return 1
}

main "$@"
