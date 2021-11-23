# shellcheck shell=bash

alias zoho-crm-prepare="observes-job-zoho-crm-prepare"

function main {
  local db_creds
  local zoho_creds

  db_creds=$(mktemp) \
    && zoho_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
      zoho_crm_bulk_creator_creds \
    && echo '[INFO] Generating secret files' \
    && echo "${zoho_crm_bulk_creator_creds}" > "${zoho_creds}" \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && zoho-crm-prepare \
      "${db_creds}" \
      "${zoho_creds}" \
      "zoho_crm_prepare"
}

main
