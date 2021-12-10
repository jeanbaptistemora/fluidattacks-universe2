# shellcheck shell=bash

function main {
  local env="${1:-}"

  source __argIntegratesBackEnv__/template "${env}" \
    && if test "${env}" = 'prod'; then
      DAEMON=true integrates-cache
    else
      DAEMON=true integrates-cache \
        && DAEMON=true dynamodb-for-integrates \
        && DAEMON=true integrates-storage
    fi \
    && pushd integrates \
    && python3 \
      back/src/cli/invoker.py \
      subscriptions.domain.trigger_subscriptions_analytics_daily \
    && popd \
    || return 1
}

main "${@}"
