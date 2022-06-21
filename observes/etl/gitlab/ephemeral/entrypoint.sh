# shellcheck shell=bash

function start_etl {
  local schema="${1}"
  local project="${2}"
  local api_key="${3}"
  local db_creds="${4}"

  echo '[INFO] Starting ephemeral ETL' \
    && echo '[INFO] Running tap' \
    && tap-gitlab v2 stream 'issues' \
      --project "${project}" \
      --api-key "${api_key}" \
      > .singer \
    && tap-gitlab v2 stream 'members' \
      --project "${project}" \
      --api-key "${api_key}" \
      >> .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --drop-schema \
      --auth "${db_creds}" \
      --schema-name "${schema}" \
      < .singer \
    && rm .singer
}

start_etl "${@}"
