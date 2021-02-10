# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'

function job_zoho_crm {

  local tap_csv
  local tap_json
  local target_redshift
  local streamer_zoho_crm

  local db_creds
  local zoho_creds

  streamer_zoho_crm="__envStreamerZohoCrm__" \
  &&  tap_csv="__envTapCsv__" \
  &&  tap_json="__envTapJson__" \
  &&  target_redshift="__envTargetRedshift__" \
  &&  db_creds=$(mktemp) \
  &&  zoho_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
        zoho_crm_etl_creds \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${zoho_crm_etl_creds}" > "${zoho_creds}" \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  "${streamer_zoho_crm}" stream "${zoho_creds}" "${db_creds}" \
        | "${tap_csv}"  | "${tap_json}"  > .singer \
  &&  "${target_redshift}" \
        --auth "${db_creds}" \
        --schema-name 'zoho_crm_test' \
        --drop-schema \
        < .singer
}

job_zoho_crm
