# shellcheck shell=bash

alias tap-dynamo="observes-singer-tap-dynamo-bin"
alias tap-json="observes-singer-tap-json-bin"

function dynamodb_etl {
  local schema="${1}"
  local tables="${2}"
  local segments="${3}"
  local db_creds

  db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && echo '[INFO] Generating secret files' \
    && json_db_creds "${db_creds}" \
    && export_notifier_key \
    && echo '[INFO] Running streamer' \
    && tap-dynamo stream \
      --tables "${tables}" \
      --segments "${segments}" \
    | tap-json \
      --date-formats '%Y-%m-%d %H:%M:%S' \
      > data \
    && target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name "${schema}" \
      < data \
    && job-last-success compound-job \
      --auth "${db_creds}" \
      --job "dynamo" \
      --child "${schema#dynamodb_}"
}

dynamodb_etl "${@}"
