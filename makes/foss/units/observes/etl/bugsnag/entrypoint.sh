# shellcheck shell=bash

alias last-success="observes-bin-service-job-last-success"
alias tap-bugsnag="observes-singer-tap-bugsnag-bin"
alias tap-json="observes-tap-json"
alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
      bugsnag_api_key \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
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
    && last-success single-job \
      --auth "${db_creds}" \
      --job 'bugsnag'
}

start_etl
