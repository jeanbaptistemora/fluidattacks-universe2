# shellcheck shell=bash

alias tap-checkly="observes-singer-tap-checkly-bin"
alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"
alias job-last-success="observes-service-job-last-success-bin"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
      checkly_api_key \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && echo '[INFO] Running tap' \
    && tap-checkly stream \
      --api-key "${checkly_api_key}" \
      --all-streams \
    | tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'checkly' \
      < .singer \
    && job-last-success single-job \
      --auth "${db_creds}" \
      --job 'checkly'
}

start_etl
