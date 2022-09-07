# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

alias code-etl="observes-etl-code-bin"

function migration {
  local namespace="${1}"
  local db
  local creds

  db=$(mktemp) \
    && creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
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
