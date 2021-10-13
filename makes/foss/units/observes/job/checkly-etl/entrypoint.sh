# shellcheck shell=bash

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
    && observes-bin-tap-checkly stream \
      --api-key "${checkly_api_key}" \
      --all-streams \
    | observes-tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && observes-target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'checkly' \
      < .singer \
    && observes-bin-service-job-last-success single-job \
      --auth "${db_creds}" \
      --job 'checkly'
}

start_etl
