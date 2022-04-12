# shellcheck shell=bash

alias zoho-crm-prepare="observes-etl-zoho-crm-prepare"

function main {
  local db_creds
  local zoho_creds

  db_creds=$(mktemp) \
    && zoho_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      zoho_crm_bulk_creator_creds \
    && echo '[INFO] Generating secret files' \
    && echo "${zoho_crm_bulk_creator_creds}" > "${zoho_creds}" \
    && json_db_creds "${db_creds}" \
    && zoho-crm-prepare \
      "${db_creds}" \
      "${zoho_creds}" \
      "zoho_crm_prepare"
}

main
