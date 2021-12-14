# shellcheck shell=bash

alias tap-dynamo="observes-bin-streamer-dynamodb"
alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"
alias job-last-success="observes-service-job-last-success-bin"

function dynamodb_etl {
  local conf="${1}"
  local schema="${2}"
  local db_creds
  local dynamo_creds

  db_creds=$(mktemp) \
    && dynamo_creds=$(mktemp) \
    && aws_login_prod_new 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
    && echo '[INFO] Generating secret files' \
    && {
      echo '{'
      echo "\"AWS_ACCESS_KEY_ID\":\"${AWS_ACCESS_KEY_ID}\","
      echo "\"AWS_SECRET_ACCESS_KEY\":\"${AWS_SECRET_ACCESS_KEY}\","
      echo "\"AWS_DEFAULT_REGION\":\"${AWS_DEFAULT_REGION}\""
      echo '}'
    } > "${dynamo_creds}" \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && echo '[INFO] Running streamer' \
    && mkdir ./logs \
    && tap-dynamo \
      --auth "${dynamo_creds}" \
      --conf "${conf}" \
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
