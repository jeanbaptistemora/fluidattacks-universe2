# shellcheck shell=bash

function main {
  local db_data="${1}"
  local integrates_daemon="${2:-true}"
  export CI_COMMIT_REF_NAME
  local host="127.0.0.1"
  local port="8022"

  DAEMON=true POPULATE=false integrates-db \
    && DAEMON=true POPULATE=false integrates-storage \
    && DAEMON=true integrates-cache \
    && for data in "${db_data}/"*'.json'; do
      echo "[INFO] Writing data from: ${data}" \
        && aws dynamodb batch-write-item \
          --endpoint-url "http://${host}:${port}" \
          --request-items "file://${data}" \
        || return 1
    done \
    && DAEMON="${integrates_daemon}" integrates-back dev
}

main "${@}"
