# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local env="${1:-}"

  source __argIntegratesBackEnv__/template "${env}" \
    && if test "${env}" = 'prod'; then
      ensure_gitlab_env_vars \
        INTEGRATES_API_TOKEN
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
      "s3://integrates/analytics/${CI_COMMIT_REF_NAME}/snapshots" \
    && popd \
    || return 1
}

main "${@}"
