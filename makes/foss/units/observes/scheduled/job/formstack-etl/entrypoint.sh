# shellcheck shell=bash

alias tap-formstack="observes-singer-tap-formstack-bin"
alias target-redshift="observes-target-redshift"
alias job-last-success="observes-bin-service-job-last-success"

function start_etl {
  local formstack_creds
  local db_creds

  db_creds=$(mktemp) \
    && formstack_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
      analytics_auth_formstack \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_formstack}" > "${formstack_creds}" \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
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
      --auth "${db_creds}" \
      --job 'formstack'
}

start_etl
