# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

alias zoho-crm-etl="observes-etl-zoho-crm"

function start_etl {
  local db_creds
  local zoho_creds

  db_creds=$(mktemp) \
    && zoho_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && export_notifier_key \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      zoho_crm_etl_creds \
    && echo '[INFO] Generating secret files' \
    && echo "${zoho_crm_etl_creds}" > "${zoho_creds}" \
    && json_db_creds "${db_creds}" \
    && zoho-crm-etl \
      "${db_creds}" \
      "${zoho_creds}" \
      "zoho_crm" \
      "zoho_crm_etl"
}

start_etl
