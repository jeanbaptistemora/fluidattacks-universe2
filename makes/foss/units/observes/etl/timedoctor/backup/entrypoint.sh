# shellcheck shell=bash

alias tap-timedoctor="observes-singer-tap-timedoctor-bin"
alias job-last-success="observes-service-job-last-success-bin"

function job_timedoctor_backup {
  local start_date
  local end_date

  local ca_file
  local wl_file

  local db_creds
  local timedoctor_creds

  db_creds=$(mktemp) \
    && timedoctor_creds=$(mktemp) \
    && start_date=$(date -d "$(date +%m)/1 -1 month" "+%Y-%m-%d") \
    && end_date=$(date -d "$(date +%m)/1 +0 month - 1 day" "+%Y-%m-%d") \
    && ca_file="timedoctor.computer_activity.${start_date}.${end_date}.singer" \
    && wl_file="timedoctor.worklogs.${start_date}.${end_date}.singer" \
    && mkdir ./logs \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
      analytics_s3_cache_timedoctor \
    && analytics_auth_timedoctor=$(
      get_project_variable \
        "${PRODUCT_API_TOKEN}" \
        "${CI_PROJECT_ID}" \
        "analytics_auth_timedoctor"
    ) \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_s3_cache_timedoctor}" > ./s3_files.json \
    && echo "${analytics_auth_timedoctor}" > "${timedoctor_creds}" \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && echo '[INFO] Running tap for worklogs' \
    && tap-timedoctor \
      --auth "${timedoctor_creds}" \
      --start-date "${start_date}" \
      --end-date "${end_date}" \
      --work-logs \
      > wl.singer \
    && echo '[INFO] Running tap for computer_activity' \
    && tap-timedoctor \
      --auth "${timedoctor_creds}" \
      --start-date "${start_date}" \
      --end-date "${end_date}" \
      --computer-activity \
      > ca.singer \
    && echo "[INFO] Uploading backup to s3" \
    && bucket=$(jq < s3_files.json -r '.bucket_name') \
    && cont_folder=$(jq < s3_files.json -r '.folder_name') \
    && aws s3 cp wl.singer "s3://${bucket}/${cont_folder}/${wl_file}" \
    && aws s3 cp ca.singer "s3://${bucket}/${cont_folder}/${ca_file}" \
    && job-last-success single-job \
      --auth "${db_creds}" \
      --job 'timedoctor_backup'
}

job_timedoctor_backup
