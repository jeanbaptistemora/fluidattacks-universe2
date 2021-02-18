# shellcheck shell=bash

function main {
  local env="${1:-}"

      source __envIntegratesEnv__ "${env}" \
  &&  if test "${env}" = 'prod'
      then
        DAEMON=true integrates-cache
      else
            DAEMON=true integrates-cache \
        &&  DAEMON=true integrates-db \
        &&  DAEMON=true integrates-storage
      fi \
  &&  pushd integrates \
    &&  envGeckoDriver='__envGeckoDriver__' \
        envFirefox='__envFirefox__' \
        RESULTS_DIR='analytics/collector/reports' \
        python3 analytics/collector/generate_reports.py \
    &&  aws_s3_sync \
          'analytics/collector' \
          "s3://fluidintegrates.analytics/${CI_COMMIT_REF_NAME}/snapshots" \
  &&  popd \
  ||  return 1
}

main "${@}"
