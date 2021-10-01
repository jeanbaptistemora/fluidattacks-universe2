# shellcheck shell=bash

function main {
  export INTEGRATES_DEPLOYMENT_DATE

  INTEGRATES_DEPLOYMENT_DATE="$(date -u '+%FT%H:%M:%SZ')" \
    && pushd integrates/front \
    && rm -rf node_modules \
    && copy "__envSetupIntegratesFrontDevRuntime__/node_modules" node_modules \
    && npm start \
    && popd \
    || return 1
}

main "${@}"
