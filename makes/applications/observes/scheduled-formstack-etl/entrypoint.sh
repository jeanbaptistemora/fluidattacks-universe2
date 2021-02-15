# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'

function job_formstack_etl {
  local tap_formstack
  local target_redshift
  local formstack_creds
  local db_creds
  local update_sync_date

  tap_formstack="__envTapFormstack__" \
  &&  target_redshift="__envTargetRedshift__" \
  &&  update_sync_date="__envUpdateSyncDate__" \
  &&  db_creds=$(mktemp) \
  &&  formstack_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
        analytics_auth_formstack \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_formstack}" > "${formstack_creds}" \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  echo '[INFO] Running tap' \
  &&  mkdir ./logs \
  &&  "${tap_formstack}" \
        --auth "${formstack_creds}" \
        --conf ./observes/conf/formstack.json \
        > .singer \
  &&  echo '[INFO] Running target' \
  &&  "${target_redshift}" \
        --auth "${db_creds}" \
        --drop-schema \
        --schema-name 'formstack' \
        < .singer \
  &&  "${update_sync_date}" "formstack" \
          --auth-file "${db_creds}"
}

job_formstack_etl
