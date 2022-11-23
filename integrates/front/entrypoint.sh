# shellcheck shell=bash

function main {
  local action="${1:-start}"
  export FI_WEBPACK_TLS_CERT=__argCertsDevelopment__/cert.crt
  export FI_WEBPACK_TLS_KEY=__argCertsDevelopment__/cert.key
  export INTEGRATES_DEPLOYMENT_DATE

  : \
    && INTEGRATES_DEPLOYMENT_DATE="$(date -u '+%FT%H:%M:%SZ')" \
    && pushd integrates/front \
    && rm -rf node_modules \
    && copy __argRuntime__ node_modules \
    && npm run "${action}" \
    && popd \
    || return 1
}

main "${@}"
