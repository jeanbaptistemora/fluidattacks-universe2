# shellcheck shell=bash

function get_schemas {
  local use_cache="${1}"
  local cache_bucket_folder="${2}"
  local input_data="${3}"
  local out_data="${4}"
  local out_folder="${5}"
  export AWS_DEFAULT_REGION="us-east-1"

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
  local schema="${1}"
  local cache_bucket="${2}"

  local db_creds
  local data
  local singer_file
  local schemas
  export AWS_DEFAULT_REGION="us-east-1"

  db_creds=$(mktemp) \
    && schemas=$(mktemp -d) \
    && singer_file=$(mktemp) \
    && data=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && export_notifier_key \
    && get_schemas "yes" "${cache_bucket}" "${data}" "${singer_file}" "${schemas}" \
    && target-redshift destroy-and-upload \
      --schema-name "${schema}" \
      < "${singer_file}"
}

dynamodb_etl "${@}"
