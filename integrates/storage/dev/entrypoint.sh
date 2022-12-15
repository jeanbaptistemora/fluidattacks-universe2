# shellcheck shell=bash

function main {
  local args=(
    "/${CI_COMMIT_REF_NAME}"
    "--exclude" "${CI_COMMIT_REF_NAME}-batch/*"
    "--exclude" "${CI_COMMIT_REF_NAME}-charts-documents/*"
    "--exclude" "${CI_COMMIT_REF_NAME}-charts-snapshots/*"
    "--exclude" "${CI_COMMIT_REF_NAME}-subscriptions-analytics/*"
    "--exclude" "${CI_COMMIT_REF_NAME}-test-functional-*/*"
    "--exclude" "${CI_COMMIT_REF_NAME}-test-unit-*/*"
  )

  populate_storage "${args[@]}"
}

main "${@}"
