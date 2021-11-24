# shellcheck shell=bash

alias tap-toe-files="observes-singer-tap-toe-files-bin"
alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && echo '[INFO] Cloning services repository' \
    && use_git_repo_services \
    && echo '[INFO] Running tap' \
    && tap-toe-files \
      > .jsonstream \
    && echo '[INFO] Running tap json' \
    && tap-json \
      > .singer \
      < .jsonstream \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'continuous_toe' \
      < .singer
}

start_etl
