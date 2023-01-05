# shellcheck shell=bash

alias tap-dynamo="observes-singer-tap-dynamo-bin"

alias target-redshift="observes-target-redshift"

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
  local schema="${1}"
  local tables="${2}"
  local segments="${3}"
  local use_cache="${4}"
  local cache_bucket="${5}"

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
    && echo '[INFO] Running streamer' \
    && tap-dynamo stream \
      --tables "${tables}" \
      --segments "${segments}" \
      > "${data}" \
    && get_schemas "${use_cache}" "${cache_bucket}" "${data}" "${singer_file}" "${schemas}" \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name "${schema}" \
      < "${singer_file}" \
    && job-last-success compound-job \
      --job "dynamo" \
      --child "${schema#dynamodb_}"
}

dynamodb_etl "${@}"
