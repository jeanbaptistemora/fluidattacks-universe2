# shellcheck shell=bash

alias last-success="observes-service-job-last-success-bin"
alias tap-announcekit="observes-singer-tap-announcekit-bin"
alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"

function start_etl {
  aws_login_dev \
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
