# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'

function job_formstack_etl {
  local tap_formstack
  local target_redshift
  local temp_file1
  local temp_file2

  tap_formstack="__envTapFormstack__" \
  &&  target_redshift="__envTargetRedshift__" \
  &&  temp_file1=$(mktemp) \
  &&  temp_file2=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
        analytics_auth_formstack \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_formstack}" > "${temp_file1}" \
  &&  echo "${analytics_auth_redshift}" > "${temp_file2}" \
  &&  echo '[INFO] Running tap' \
  &&  mkdir ./logs \
  &&  "${tap_formstack}" \
        --auth "${temp_file1}" \
        --conf ./observes/conf/formstack.json \
        > .singer \
  &&  echo '[INFO] Running target' \
  &&  "${target_redshift}" \
        --auth "${temp_file2}" \
        --drop-schema \
        --schema-name 'formstack' \
        < .singer
}

job_formstack_etl
