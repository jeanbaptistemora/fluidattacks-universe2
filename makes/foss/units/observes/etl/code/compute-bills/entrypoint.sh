# shellcheck shell=bash

alias code-etl="observes-bin-code-etl"

function job_compute_bills {
  local bucket_month
  local bucket_day
  local folder

  aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && folder="$(mktemp -d)" \
    && bucket_month="s3://continuous-data/bills/$(date +%Y)/$(date +%m)" \
    && bucket_day="s3://continuous-data/bills/$(date +%Y)/$(date +%m)/$(date +%d)" \
    && echo "[INFO] Temporary results folder: ${folder}" \
    && code-etl compute-bills \
      "${folder}" \
      "$(date +%Y)" \
      "$(date +%m)" \
      "${INTEGRATES_API_TOKEN}" \
    && aws_login_prod 'services' \
    && echo "[INFO] Syncing data from: ${folder} to ${bucket_month}" \
    && aws_s3_sync "${folder}" "${bucket_month}" \
    && echo "[INFO] Syncing data from: ${folder} to ${bucket_day}" \
    && aws_s3_sync "${folder}" "${bucket_day}"
}

job_compute_bills
