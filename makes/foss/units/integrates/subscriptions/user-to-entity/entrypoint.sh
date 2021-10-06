# shellcheck shell=bash

function main {
  local env="${1:-}"
  local api_status="migration"

  source __argIntegratesBackEnv__/template "${env}" "${api_status}" \
    && if test "${env}" = 'prod'; then
      DAEMON=true integrates-cache
    else
      DAEMON=true integrates-cache \
        && DAEMON=true integrates-db \
        && DAEMON=true integrates-storage
    fi \
    && pushd integrates \
    && python3 \
      back/src/cli/invoker.py \
      subscriptions.domain.trigger_user_to_entity_report \
    && popd \
    || return 1
}

main "${@}"
