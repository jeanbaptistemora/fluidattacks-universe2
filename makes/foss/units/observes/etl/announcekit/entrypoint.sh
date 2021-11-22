# shellcheck shell=bash

alias last-success="observes-bin-service-job-last-success"
alias tap-announcekit="observes-singer-tap-announcekit-bin"
alias tap-json="observes-tap-json"
alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      announcekit_user \
      announcekit_passwd \
      announcekit_fluid_proj \
      analytics_auth_redshift \
    && export ANNOUNCEKIT_USER="${announcekit_user}" \
    && export ANNOUNCEKIT_PASSWD="${announcekit_passwd}" \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && echo '[INFO] Running tap' \
    && tap-announcekit stream 'ALL' \
      --project "${announcekit_fluid_proj}" \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'announcekit' \
      < .singer \
    && last-success single-job \
      --auth "${db_creds}" \
      --job 'announcekit'
}

start_etl
