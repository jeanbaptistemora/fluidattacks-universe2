# shellcheck shell=bash

function job_zoho_prepare {
  local db_creds
  local zoho_creds

      db_creds=$(mktemp) \
  &&  zoho_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
        zoho_crm_bulk_creator_creds \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${zoho_crm_bulk_creator_creds}" > "${zoho_creds}" \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  observes-bin-streamer-zoho-crm init-db "${db_creds}" \
  &&  observes-bin-streamer-zoho-crm create-jobs "${zoho_creds}" "${db_creds}" \
  &&  observes-update-sync-date single-job \
        --auth "${db_creds}" \
        --job 'zoho_crm_prepare'
}

job_zoho_prepare
