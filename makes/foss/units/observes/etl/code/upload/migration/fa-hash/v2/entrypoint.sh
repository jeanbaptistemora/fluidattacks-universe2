# shellcheck shell=bash

alias code-etl="observes-etl-code-bin"

function migration {
  local namespace="${1}"
  local db
  local creds

  db=$(mktemp) \
    && creds=$(mktemp) \
    && aws_login_prod_new 'observes' \
    && prod_db "${db}" \
    && prod_user "${creds}" \
    && code-etl \
      --db-id "${db}" \
      --creds "${creds}" \
      migration calculate-fa-hash \
      "${namespace}" \
      --source "code" "commits" \
      --target "code" "migrated"
}

migration "${@}"
