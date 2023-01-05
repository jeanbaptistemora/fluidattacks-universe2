# shellcheck shell=bash

alias tap-zoho-crm="observes-singer-tap-zoho-crm-bin"

function main {
  local db_creds="${1}"
  local zoho_creds="${2}"
  local job_name="${3}"

  tap-zoho-crm init-db \
    "${db_creds}" \
    && tap-zoho-crm create-jobs \
      "${zoho_creds}" \
      "${db_creds}" \
    && success-indicators single-job \
      --job "${job_name}"
}

main "${@}"
