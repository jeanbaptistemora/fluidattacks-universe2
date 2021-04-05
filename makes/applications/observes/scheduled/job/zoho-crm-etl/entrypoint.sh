# shellcheck shell=bash

function job_zoho_crm {
  local db_creds
  local zoho_creds

      db_creds=$(mktemp) \
  &&  zoho_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
        zoho_crm_etl_creds \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${zoho_crm_etl_creds}" > "${zoho_creds}" \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  observes-bin-streamer-zoho-crm stream "${zoho_creds}" "${db_creds}" \
        | observes-bin-tap-csv \
        | observes-tap-json \
        > .singer \
  &&  observes-target-redshift \
        --auth "${db_creds}" \
        --schema-name 'zoho_crm' \
        --drop-schema \
        < .singer \
  &&  observes-bin-service-job-last-success single-job \
        --auth "${db_creds}" \
        --job "zoho_crm_etl"
}

job_zoho_crm
