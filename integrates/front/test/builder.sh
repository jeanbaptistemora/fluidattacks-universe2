# shellcheck shell=bash

function main {
  export HOME

  HOME="$(mktemp -d)" \
    && copy "${envSrcIntegratesFront}" "${out}" \
    && copy "${envSetupIntegratesFrontDevRuntime}" "${out}/node_modules" \
    && pushd "${out}" \
    && npm run test \
    && popd \
    || return 1
}

main "${@}"
