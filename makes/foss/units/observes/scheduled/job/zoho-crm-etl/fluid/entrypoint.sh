# shellcheck shell=bash

alias zoho-crm-etl="observes-job-zoho-crm-etl"

function start_etl {
  local db_creds
  local zoho_creds

  db_creds=$(mktemp) \
    && zoho_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
      zoho_crm_etl_creds \
    && echo '[INFO] Generating secret files' \
    && echo "${zoho_crm_etl_creds}" > "${zoho_creds}" \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && zoho-crm-etl \
      "${db_creds}" \
      "${zoho_creds}" \
      "zoho_crm" \
      "zoho_crm_etl"
}

start_etl
