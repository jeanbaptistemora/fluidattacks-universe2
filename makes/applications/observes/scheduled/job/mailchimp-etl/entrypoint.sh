# shellcheck shell=bash

function start_etl {
  local db_creds
  local mailchimp_creds

  db_creds=$(mktemp) \
    && mailchimp_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      mailchimp_api_key \
      mailchimp_dc \
      analytics_auth_redshift \
    && {
      echo '{'
      echo "\"api_key\":\"${mailchimp_api_key}\","
      echo "\"dc\":\"${mailchimp_dc}\""
      echo '}'
    } > "${mailchimp_creds}" \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && echo '[INFO] Running tap' \
    && observes-bin-tap-mailchimp stream \
      --creds-file "${mailchimp_creds}" \
      --all-streams \
    | observes-tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && observes-target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'mailchimp' \
      < .singer \
    && observes-bin-service-job-last-success single-job \
      --auth "${db_creds}" \
      --job 'mailchimp'
}

start_etl
