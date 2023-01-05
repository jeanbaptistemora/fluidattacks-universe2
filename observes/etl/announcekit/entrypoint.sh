# shellcheck shell=bash

alias tap-announcekit="observes-singer-tap-announcekit-bin"

alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      announcekit_user \
      announcekit_passwd \
      announcekit_fluid_proj \
      bugsnag_notifier_key \
    && export ANNOUNCEKIT_USER="${announcekit_user}" \
    && export ANNOUNCEKIT_PASSWD="${announcekit_passwd}" \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
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
    && job-last-success single-job \
      --job 'announcekit'
}

start_etl
