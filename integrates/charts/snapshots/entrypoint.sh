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
    && envGeckoDriver='__argGeckoDriver__' \
      envFirefox='__argFirefox__' \
      RESULTS_DIR='charts/collector/reports' \
      python3 charts/collector/generate_reports.py \
    && aws_s3_sync \
      'charts/collector' \
      "s3://fluidintegrates.analytics/${CI_COMMIT_REF_NAME}/snapshots" \
    && popd \
    || return 1
}

main "${@}"
