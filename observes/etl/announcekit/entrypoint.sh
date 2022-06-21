# shellcheck shell=bash

alias tap-announcekit="observes-singer-tap-announcekit-bin"
alias tap-json="observes-singer-tap-json-bin"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
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
    && tap-announcekit stream 'PROJECTS' \
      --project "${announcekit_fluid_proj}" \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'announcekit_test' \
      < .singer
}

start_etl
