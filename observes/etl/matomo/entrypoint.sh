# shellcheck shell=bash

alias tap-matomo="observes-singer-tap-matomo-bin"
alias target-redshift="observes-target-redshift"

function job_matomo {
  local db_creds

  db_creds=$(mktemp) \
    && mkdir ./logs \
    && export_notifier_key \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      MATOMO_API_TOKEN \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && echo '[INFO] Running tap' \
    && tap-matomo \
      --end-date "$(date +"%Y-%m-%d")" \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'matomo' \
      < .singer \
    && success-indicators single-job \
      --job 'matomo'
}

job_matomo
