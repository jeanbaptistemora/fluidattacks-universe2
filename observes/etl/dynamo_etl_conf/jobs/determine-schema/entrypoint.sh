# shellcheck shell=bash

alias tap-dynamo="observes-singer-tap-dynamo-bin"

function determine_schemas {
  local tables="${1}"
  local segments="${2}"
  local cache_bucket="${3}"

  local db_creds
  local schemas
  export AWS_DEFAULT_REGION="us-east-1"

  db_creds=$(mktemp) \
    && schemas=$(mktemp -d) \
    && aws_login "prod_observes" "3600" \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && echo '[INFO] Starting local dynamo...' \
    && { DAEMON=true dynamodb & } \
    && sleep 60 \
    && echo '[INFO] Local dynamo runing' \
    && export_notifier_key \
    && echo '[INFO] Determining data schemas from data...' \
    && tap-dynamo stream \
      --tables "${tables}" \
      --segments "${segments}" \
      --endpoint-url "http://localhost:8022" \
      --use-ssl "true" \
      --verify "true" \
    | tap-json \
      --date-formats '%Y-%m-%d %H:%M:%S' \
      --schema-folder "${schemas}" \
      --not-dump-records \
    && echo '[INFO] Saving schemas...' \
    && aws_s3_sync "${schemas}" "${cache_bucket}" \
    && echo '[INFO] Schemas saved!'
}

determine_schemas "${@}"
