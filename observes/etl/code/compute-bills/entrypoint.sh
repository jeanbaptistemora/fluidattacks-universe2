# shellcheck shell=bash

function job_compute_bills {
  local bucket_month
  local bucket_day
  local folder
  local db
  local creds

  db=$(mktemp) \
    && creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && prod_db "${db}" \
    && prod_user "${creds}" \
    && export_notifier_key \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && folder="$(mktemp -d)" \
    && bucket_month="s3://integrates/continuous-data/bills/$(date +%Y)/$(date +%m)" \
    && bucket_day="s3://integrates/continuous-data/bills/$(date +%Y)/$(date +%m)/$(date +%d)" \
    && echo "[INFO] Temporary results folder: ${folder}" \
    && observes-etl-code \
      --db-id "${db}" \
      --creds "${creds}" \
      compute-bills \
      "${folder}" \
      "$(date +%Y)" \
      "$(date +%m)" \
      "${INTEGRATES_API_TOKEN}" \
    && success-indicators single-job \
      --job 'compute_bills' \
    && echo "[INFO] Syncing data from: ${folder} to ${bucket_month}" \
    && aws_s3_sync "${folder}" "${bucket_month}" \
    && echo "[INFO] Syncing data from: ${folder} to ${bucket_day}" \
    && aws_s3_sync "${folder}" "${bucket_day}"
}

job_compute_bills
