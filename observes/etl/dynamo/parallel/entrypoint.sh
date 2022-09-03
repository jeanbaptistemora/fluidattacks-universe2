# shellcheck shell=bash

alias tap-dynamo="observes-singer-tap-dynamo-bin"
alias tap-json="observes-singer-tap-json-bin"

function get_schemas {
  local use_cache="${1}"
  local cache_bucket_folder="${2}"
  local input_data="${3}"
  local out_data="${4}"
  local out_folder="${5}"

  if test "${use_cache}" == "yes"; then
    echo "[INFO] Using schemas cache at ${cache_bucket_folder}" \
      && aws_s3_sync "${cache_bucket_folder}" "${out_folder}" \
      && tap-json \
        --date-formats '%Y-%m-%d %H:%M:%S' \
        --schema-folder "${out_folder}" \
        --schema-cache \
        < "${input_data}" \
        > "${out_data}"
  else
    echo '[INFO] Determining data schemas...' \
      && tap-json \
        --date-formats '%Y-%m-%d %H:%M:%S' \
        --schema-folder "${out_folder}" \
        < "${input_data}" \
        > "${out_data}" \
      && if test "${cache_bucket_folder}" != "none"; then
        echo '[INFO] Saving schemas...' \
          && aws_s3_sync "${out_folder}" "${cache_bucket_folder}" \
          && echo '[INFO] Schemas saved!'
      fi
  fi || return 1
}

function dynamodb_etl {
  local total_segments="${1}"
  local segment="${2}"

  local db_creds
  local data
  local singer_file
  local schemas
  export AWS_DEFAULT_REGION="us-east-1"

  if test "${segment}" == "auto"; then
    segment="${AWS_BATCH_JOB_ARRAY_INDEX}"
  fi \
    && echo "[INFO] worker at segment: ${segment}" \
    && db_creds=$(mktemp) \
    && schemas=$(mktemp -d) \
    && singer_file=$(mktemp) \
    && data=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && export_notifier_key \
    && echo '[INFO] Running segment streamer' \
    && tap-dynamo stream-segment \
      --table "integrates_vms" \
      --current "${segment}" \
      --total "${total_segments}" \
      > "${data}" \
    && get_schemas "yes" "s3://observes.cache/dynamoEtl/vms_schema" "${data}" "${singer_file}" "${schemas}" \
    && echo "[INFO] Singer file at ${singer_file}" \
    && echo '[INFO] Running target-s3' \
    && target-s3 \
      --bucket 'observes.etl-data' \
      --prefix "dynamodb/part_${segment}/" \
      < "${singer_file}" \
    && echo '[INFO] Running target-redshift' \
    && target-redshift from-s3 \
      --schema-name "dynamodb_integrates_vms_part_${segment}" \
      --bucket 'observes.etl-data' \
      --prefix "dynamodb/part_${segment}/" \
      --role 'arn:aws:iam::205810638802:role/redshift-role' \
      < "${singer_file}"
}

dynamodb_etl "${@}"
