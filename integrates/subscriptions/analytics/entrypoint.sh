# shellcheck shell=bash

function main {
  local env="${1:-}"
  local report_frequency="${2:-}"

  source __argIntegratesBackEnv__/template "${env}" \
    && if test "${env}" = 'dev'; then
      DAEMON=true integrates-db \
        && populate_storage
    fi \
    && pushd integrates \
    && python3 \
      back/src/cli/invoker.py \
      subscriptions.domain.trigger_subscriptions_analytics \
      "${report_frequency}" \
    && popd \
    || return 1
}

main "${@}"
