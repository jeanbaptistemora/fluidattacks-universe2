# shellcheck shell=bash

alias tap-zoho-crm="observes-bin-streamer-zoho-crm"
alias tap-csv="observes-singer-tap-csv-bin"
alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"
alias job-last-success="observes-service-job-last-success-bin"

function start_etl {
  local db_creds="${1}"
  local zoho_creds="${2}"
  local target_schema="${3}"
  local job_name="${4}"

  tap-zoho-crm stream "${zoho_creds}" "${db_creds}" \
    | tap-csv \
    | tap-json \
      > .singer \
    && target-redshift \
      --auth "${db_creds}" \
      --schema-name "${target_schema}" \
      --drop-schema \
      --old-ver \
      < .singer \
    && job-last-success single-job \
      --auth "${db_creds}" \
      --job "${job_name}"
}

start_etl "${@}"
