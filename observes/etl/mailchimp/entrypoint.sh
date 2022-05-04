# shellcheck shell=bash

alias job-success="observes-service-job-last-success-bin"
alias tap-mailchimp="observes-singer-tap-mailchimp-bin"
alias tap-json="observes-singer-tap-json-bin"
alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds
  local mailchimp_creds

  db_creds=$(mktemp) \
    && mailchimp_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && export_notifier_key \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      mailchimp_api_key \
      mailchimp_dc \
    && {
      echo '{'
      echo "\"api_key\":\"${mailchimp_api_key}\","
      echo "\"dc\":\"${mailchimp_dc}\""
      echo '}'
    } > "${mailchimp_creds}" \
    && json_db_creds "${db_creds}" \
    && echo '[INFO] Running tap' \
    && tap-mailchimp stream \
      --creds-file "${mailchimp_creds}" \
      --all-streams \
    | tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'mailchimp' \
      < .singer \
    && job-success single-job \
      --auth "${db_creds}" \
      --job 'mailchimp'
}

start_etl
