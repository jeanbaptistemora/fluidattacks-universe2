# shellcheck shell=bash

function main {
  local db_creds="${1}"
  local zoho_creds="${2}"
  local job_name="${3}"

  observes-bin-streamer-zoho-crm init-db \
    "${db_creds}" \
    && observes-bin-streamer-zoho-crm create-jobs \
      "${zoho_creds}" \
      "${db_creds}" \
    && observes-bin-service-job-last-success single-job \
      --auth "${db_creds}" \
      --job "${job_name}"
}

main "${@}"
