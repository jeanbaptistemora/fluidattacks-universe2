# shellcheck shell=bash

alias code-etl="observes-etl-code-bin"

function migration {
  local db
  local creds

  db=$(mktemp) \
    && creds=$(mktemp) \
    && aws_login_prod_new 'observes' \
    && prod_db "${db}" \
    && prod_user "${creds}" \
    && code-etl v2 \
      --db-id "${db}" \
      --creds "${creds}" \
      migration calculate-fa-hash-2 \
      --source "code" "commits" \
      --target "code" "migrated"
}

migration
