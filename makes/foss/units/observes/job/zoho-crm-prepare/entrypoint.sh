# shellcheck shell=bash

alias tap-zoho-crm="observes-bin-streamer-zoho-crm"
alias job-last-success="observes-bin-service-job-last-success"

function main {
  local db_creds="${1}"
  local zoho_creds="${2}"
  local job_name="${3}"

  tap-zoho-crm init-db \
    "${db_creds}" \
    && tap-zoho-crm create-jobs \
      "${zoho_creds}" \
      "${db_creds}" \
    && job-last-success single-job \
      --auth "${db_creds}" \
      --job "${job_name}"
}

main "${@}"
