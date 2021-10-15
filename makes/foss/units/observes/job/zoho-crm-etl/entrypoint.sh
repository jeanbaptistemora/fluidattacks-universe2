# shellcheck shell=bash

function start_etl {
  local db_creds="${1}"
  local zoho_creds="${2}"
  local target_schema="${3}"
  local job_name="${4}"

  observes-bin-streamer-zoho-crm stream "${zoho_creds}" "${db_creds}" \
    | observes-bin-tap-csv \
    | observes-tap-json \
      > .singer \
    && observes-target-redshift \
      --auth "${db_creds}" \
      --schema-name "${target_schema}" \
      --drop-schema \
      --old-ver \
      < .singer \
    && observes-bin-service-job-last-success single-job \
      --auth "${db_creds}" \
      --job "${job_name}"
}

start_etl "${@}"
