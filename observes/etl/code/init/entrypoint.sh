# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local db
  local creds
  export AWS_DEFAULT_REGION="us-east-1"

  db=$(mktemp) \
    && creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && prod_db "${db}" \
    && prod_user "${creds}" \
    && observes-etl-code \
      --db-id "${db}" \
      --creds "${creds}" \
      init-table "${@}"
}

main "${@}"
