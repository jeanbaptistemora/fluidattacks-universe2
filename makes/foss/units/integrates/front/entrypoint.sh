# shellcheck shell=bash

function main {
  local action="${1:-start}"
  export INTEGRATES_DEPLOYMENT_DATE

  INTEGRATES_DEPLOYMENT_DATE="$(date -u '+%FT%H:%M:%SZ')" \
    && pushd integrates/front \
    && rm -rf node_modules \
    && copy __argSetupIntegratesFrontDevRuntime__ node_modules \
    && npm run "${action}" \
    && popd \
    || return 1
}

main "${@}"
