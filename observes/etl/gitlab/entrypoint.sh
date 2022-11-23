# shellcheck shell=bash

alias target-redshift="observes-target-redshift"

function start_etl {
  local schema="${1}"
  local project="${2}"
  local state="${3}"
  local token="${4}"
  local db_creds="${5}"
  export AWS_DEFAULT_REGION="us-east-1"

  echo "[INFO] Gitlab ETL for ${project}" \
    && echo '[INFO] Running tap' \
    && tap-gitlab stream "all" \
      --project "${project}" \
      --api-key "${token}" \
      --max-pages 250 \
      --state "${state}" \
    | tap-json > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --schema-name "${schema}" \
      --state "${state}" \
      < .singer
}

start_etl "${@}"
