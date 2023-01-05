# shellcheck shell=bash

alias tap-formstack="observes-singer-tap-formstack-bin"
alias target-redshift="observes-target-redshift"

function start_etl {
  local formstack_creds
  local db_creds

  db_creds=$(mktemp) \
    && formstack_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && export_notifier_key \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      analytics_auth_formstack \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_formstack}" > "${formstack_creds}" \
    && json_db_creds "${db_creds}" \
    && echo '[INFO] Running tap' \
    && mkdir ./logs \
    && tap-formstack \
      --auth "${formstack_creds}" \
      --conf ./observes/conf/formstack.json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'formstack' \
      --old-ver \
      < .singer \
    && job-last-success single-job \
      --job 'formstack'
}

start_etl
