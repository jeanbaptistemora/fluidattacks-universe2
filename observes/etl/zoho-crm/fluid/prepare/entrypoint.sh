# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

alias zoho-crm-prepare="observes-etl-zoho-crm-prepare"

function main {
  local db_creds
  local zoho_creds

  db_creds=$(mktemp) \
    && zoho_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && export_notifier_key \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      zoho_crm_bulk_creator_creds \
    && echo '[INFO] Generating secret files' \
    && echo "${zoho_crm_bulk_creator_creds}" > "${zoho_creds}" \
    && json_db_creds "${db_creds}" \
    && zoho-crm-prepare \
      "${db_creds}" \
      "${zoho_creds}" \
      "zoho_crm_prepare"
}

main
