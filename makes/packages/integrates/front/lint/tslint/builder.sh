# shellcheck shell=bash

function main {
      copy "${envSrcIntegratesFront}" "${out}" \
  &&  copy "${envSetupIntegratesFrontDevRuntime}/node_modules" "${out}/node_modules" \
  &&  pushd "${out}" \
    &&  ./node_modules/.bin/tcm src/ --silent \
    &&  ./node_modules/.bin/tsc -p tsconfig.json \
    &&  ./node_modules/.bin/tslint -p tsconfig.json -t codeFrame \
  &&  popd \
  ||  return 1
}

main "$@"
