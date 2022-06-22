# shellcheck shell=bash

alias tap-bugsnag="observes-singer-tap-bugsnag-bin"
alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      bugsnag_api_key \
      bugsnag_notifier_key \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && echo '[INFO] Running tap' \
    && tap-bugsnag stream \
      --api-key "${bugsnag_api_key}" \
      --all-streams \
    | tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'bugsnag' \
      < .singer \
    && job-last-success single-job \
      --auth "${db_creds}" \
      --job 'bugsnag'
}

start_etl
