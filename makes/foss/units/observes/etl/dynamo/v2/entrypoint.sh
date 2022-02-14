# shellcheck shell=bash

alias tap-dynamo="observes-singer-tap-dynamo-bin"
alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"
alias job-last-success="observes-service-job-last-success-bin"

function dynamodb_etl {
  local schema="${1}"
  local tables="${2}"
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod_new 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && echo '[INFO] Running streamer' \
    && tap-dynamo stream --tables "${tables}" \
    | tap-json \
      --date-formats '%Y-%m-%d %H:%M:%S' \
      | target-redshift \
        --auth "${db_creds}" \
        --drop-schema \
        --schema-name "${schema}" \
    && job-last-success compound-job \
      --auth "${db_creds}" \
      --job "dynamo" \
      --child "${schema#dynamodb_}"
}

dynamodb_etl "${@}"
