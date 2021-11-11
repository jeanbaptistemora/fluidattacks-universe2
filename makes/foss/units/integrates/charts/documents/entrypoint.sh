# shellcheck shell=bash

function execute_analytics_generator {
  local generator="${1}"
  local results_dir="${generator//.py/}"

  mkdir -p "${results_dir}" \
    && echo "[INFO] Running: ${generator}" \
    && {
      RESULTS_DIR="${results_dir}" python3 "${generator}" \
        || RESULTS_DIR="${results_dir}" python3 "${generator}" \
        || RESULTS_DIR="${results_dir}" python3 "${generator}"
    }
}

function main {
  local env="${1:-}"
  local todo

  source __argIntegratesBackEnv__/template "${env}" \
    && if test "${env}" = 'prod'; then
      DAEMON=true integrates-cache
    else
      DAEMON=true integrates-cache \
        && DAEMON=true dynamodb-for-integrates \
        && DAEMON=true integrates-storage
    fi \
    && pushd integrates \
    && todo=$(mktemp) \
    && find 'charts/generators' -wholename '*.py' | sort > "${todo}" \
    && execute_chunk_parallel execute_analytics_generator "${todo}" \
    && aws_s3_sync \
      'charts/generators' \
      "s3://fluidintegrates.analytics/${CI_COMMIT_REF_NAME}/documents" \
    && popd \
    || return 1
}

main "${@}"
