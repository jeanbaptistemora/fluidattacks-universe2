# shellcheck shell=bash

function main {
  local env="${1:-}"

  __envIntegratesScheduler__ "${env}" schedulers.update_indicators.main || return 1
}

main "${@}"
