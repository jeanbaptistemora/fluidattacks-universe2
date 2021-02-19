# shellcheck shell=bash

function dynamodb_etl {
  local conf="${1}"
  local schema="${2}"
  local db_creds
  local dynamo_creds

      db_creds=$(mktemp) \
  &&  dynamo_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_aws_access_key \
        analytics_aws_secret_key \
        analytics_aws_default_region \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  {
        echo '{'
        echo "\"AWS_ACCESS_KEY_ID\":\"${analytics_aws_access_key}\","
        echo "\"AWS_SECRET_ACCESS_KEY\":\"${analytics_aws_secret_key}\","
        echo "\"AWS_DEFAULT_REGION\":\"${analytics_aws_default_region}\""
        echo '}'
      } > "${dynamo_creds}" \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  echo '[INFO] Running streamer' \
  &&  mkdir ./logs \
  &&  observes-streamer-dynamodb \
        --auth "${dynamo_creds}" \
        --conf "${conf}" > .stream \
  &&  echo '[INFO] Running tap' \
  &&  observes-tap-json \
      --date-formats '%Y-%m-%d %H:%M:%S' \
      < .stream \
      > .singer \
  &&  echo '[INFO] Running target' \
  &&  observes-target-redshift \
        --auth "${db_creds}" \
        --drop-schema \
        --schema-name "${schema}" \
        < .singer \
  &&  observes-update-sync-date compound-job \
        --auth "${db_creds}" \
        --job "dynamo" \
        --child "${schema#dynamodb_}"
}

dynamodb_etl "${@}"
