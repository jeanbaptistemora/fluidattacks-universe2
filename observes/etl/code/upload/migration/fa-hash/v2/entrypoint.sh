# shellcheck shell=bash

function migration {
  local namespace="${1}"
  local db
  local creds

  db=$(mktemp) \
    && creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && prod_db "${db}" \
    && prod_user "${creds}" \
    && observes-etl-code \
      --db-id "${db}" \
      --creds "${creds}" \
      migration calculate-fa-hash \
      "${namespace}" \
      --source "code" "commits" \
      --target "code" "migrated"
}

migration "${@}"
