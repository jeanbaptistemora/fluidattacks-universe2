# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'

function job_zoho_prepare {
  local db_creds
  local streamer_zoho_crm
  local zoho_creds

  streamer_zoho_crm="__envStreamerZohoCrm__" \
  &&  update_sync_date="__envUpdateSyncDate__" \
  &&  db_creds=$(mktemp) \
  &&  zoho_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
        zoho_crm_bulk_creator_creds \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${zoho_crm_bulk_creator_creds}" > "${zoho_creds}" \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  "${streamer_zoho_crm}" init-db "${db_creds}" \
  &&  "${streamer_zoho_crm}" create-jobs "${zoho_creds}" "${db_creds}" \
  &&  "${update_sync_date}" zoho-crm-prepare "${db_creds}"
}

job_zoho_prepare
