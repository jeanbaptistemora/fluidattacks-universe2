# shellcheck shell=bash

alias tap-dynamo="observes-singer-tap-dynamo-bin"

function dynamodb_etl {
  local segment="${1}"

  local db_creds
  local schemas
  local cache_bucket_folder
  export AWS_DEFAULT_REGION="us-east-1"

  if test "${segment}" == "auto"; then
    segment="${AWS_BATCH_JOB_ARRAY_INDEX}"
  fi \
    && echo "[INFO] worker at segment: ${segment}" \
    && db_creds=$(mktemp) \
    && schemas=$(mktemp -d) \
    && cache_bucket_folder="s3://observes.cache/dynamoEtl/vms_schema" \
    && aws_login "prod_observes" "3600" \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && export_notifier_key \
    && echo "[INFO] Getting schemas cache at ${cache_bucket_folder}" \
    && aws_s3_sync "${cache_bucket_folder}" "${schemas}" \
    && echo '[INFO] Running Last ETL phase' \
    && tap-json \
      --date-formats '%Y-%m-%d %H:%M:%S' \
      --schema-folder "${schemas}" \
      --schema-cache \
      > .singer \
    && target-redshift from-s3 \
      --schema-name "dynamodb_integrates_vms_part_${segment}" \
      --bucket 'observes.etl-data' \
      --prefix "dynamodb/part_${segment}/" \
      --role 'arn:aws:iam::205810638802:role/redshift-role' \
      < .singer \
    && rm -f .singer
}

dynamodb_etl "${@}"
