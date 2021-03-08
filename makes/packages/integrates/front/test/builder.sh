# shellcheck shell=bash

function main {
      copy "${envSrcIntegratesFront}" "${out}" \
  &&  copy "${envSetupIntegratesFrontDevRuntime}/node_modules" "${out}/node_modules" \
  &&  pushd "${out}" \
    &&  npm test \
  &&  popd \
  || return 1
}

main "${@}"
