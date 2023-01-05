# shellcheck shell=bash

alias tap-delighted="observes-singer-tap-delighted-bin"

alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      delighted_api_key \
      bugsnag_notifier_key \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && echo '[INFO] Running tap' \
    && tap-delighted stream \
      --api-key "${delighted_api_key}" \
      --all-streams \
    | tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'delighted' \
      < .singer \
    && job-last-success single-job \
      --job 'delighted'
}

start_etl
