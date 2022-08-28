# shellcheck shell=bash

alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && export_notifier_key \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      mandrill_api_key \
    && json_db_creds "${db_creds}" \
    && echo '[INFO] Running tap' \
    && tap-mandrill stream "activity" \
      --api-key "${mandrill_api_key}" \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'mandrill' \
      < .singer
}

start_etl
