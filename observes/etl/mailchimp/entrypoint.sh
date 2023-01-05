# shellcheck shell=bash

alias tap-mailchimp="observes-singer-tap-mailchimp-bin"

alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds
  local mailchimp_creds

  db_creds=$(mktemp) \
    && mailchimp_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
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
    && success-indicators single-job \
      --job 'mailchimp'
}

start_etl
