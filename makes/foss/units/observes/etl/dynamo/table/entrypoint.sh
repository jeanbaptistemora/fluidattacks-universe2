# shellcheck shell=bash

alias dynamodb-etl="observes-etl-dynamo"

function create_config {
  local table="${1}"
  local target="${2}"

  echo "{\"tables\": [\"${table}\"]}" \
    | tr '\r\n' ' ' \
    | jq . > "${target}"
}

function table_etl {
  local table="${1}"

  conf=$(mktemp) \
    && create_config "${table}" "${conf}" \
    && dynamodb-etl "${conf}" "dynamodb_${table}"
}

table_etl "${@}"
