# shellcheck shell=bash

function main {
  local env="${1:-}"

  source __argIntegratesBackEnv__/template "${env}" \
    && if test "${env}" = 'prod'; then
      ensure_gitlab_env_vars \
        INTEGRATES_API_TOKEN
    else
      DAEMON=true integrates-db \
        && export AWS_S3_PATH_PREFIX="${CI_COMMIT_REF_NAME}-charts-snapshots/" \
        && populate_storage "/${CI_COMMIT_REF_NAME}-charts-snapshots"
    fi \
    && pushd integrates \
    && envGeckoDriver='__argGeckoDriver__' \
      envFirefox='__argFirefox__' \
      RESULTS_DIR='charts/collector/reports' \
      python3 charts/collector/generate_reports.py \
    && aws_s3_sync \
      'charts/collector' \
      "s3://integrates/analytics/${CI_COMMIT_REF_NAME}/snapshots" \
    && popd \
    || return 1
}

main "${@}"
