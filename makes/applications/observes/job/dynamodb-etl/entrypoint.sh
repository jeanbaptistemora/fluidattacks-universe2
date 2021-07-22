# shellcheck shell=bash

function dynamodb_etl {
  local conf="${1}"
  local schema="${2}"
  local db_creds
  local dynamo_creds

  db_creds=$(mktemp) \
    && dynamo_creds=$(mktemp) \
    && aws_login_prod 'observes' \
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
    && observes-bin-streamer-dynamodb \
      --auth "${dynamo_creds}" \
      --conf "${conf}" \
    | observes-tap-json \
      --date-formats '%Y-%m-%d %H:%M:%S' \
      | observes-target-redshift \
        --auth "${db_creds}" \
        --drop-schema \
        --schema-name "${schema}" \
    && observes-bin-service-job-last-success compound-job \
      --auth "${db_creds}" \
      --job "dynamo" \
      --child "${schema#dynamodb_}"
}

dynamodb_etl "${@}"
