# shellcheck shell=bash

function main {
  local args=(
    "" # No path prefix
    "--exclude" "batch/*"
    "--exclude" "charts-documents/*"
    "--exclude" "charts-snapshots/*"
    "--exclude" "subscriptions-analytics/*"
    "--exclude" "test-functional-*/*"
    "--exclude" "test-unit-*/*"
  )

  populate_storage "${args[@]}"
}

main "${@}"
