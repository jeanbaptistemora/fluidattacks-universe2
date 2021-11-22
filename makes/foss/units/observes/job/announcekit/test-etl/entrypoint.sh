# shellcheck shell=bash

alias last-success="observes-bin-service-job-last-success"
alias tap-announcekit="observes-bin-tap-announcekit"
alias tap-json="observes-tap-json"
alias target-redshift="observes-target-redshift"

function start_etl {
  aws_login_dev_new \
    && sops_export_vars 'observes/secrets-dev.yaml' \
      announcekit_user \
      announcekit_passwd \
      announcekit_proj \
    && export ANNOUNCEKIT_USER="${announcekit_user}" \
    && export ANNOUNCEKIT_PASSWD="${announcekit_passwd}" \
    && echo '[INFO] Running tap' \
    && tap-announcekit stream 'ALL' \
      --project "${announcekit_proj}" \
      > .singer
}

start_etl
