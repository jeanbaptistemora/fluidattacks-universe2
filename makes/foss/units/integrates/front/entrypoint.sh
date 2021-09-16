# shellcheck shell=bash

function main {
  export INTEGRATES_DEPLOYMENT_DATE

  INTEGRATES_DEPLOYMENT_DATE="$(date -u '+%FT%H:%M:%SZ')" \
    && pushd integrates/front \
    && rm -rf node_modules \
    && copy __argSetupIntegratesFrontDevRuntime__ node_modules \
    && for bin in webpack webpack-cli; do
      copy "$(realpath "node_modules/.bin/${bin}")" "node_modules/.bin/${bin}2" \
        && mv "node_modules/.bin/${bin}"{2,}
    done \
    && npm start \
    && popd \
    || return 1
}

main "${@}"
