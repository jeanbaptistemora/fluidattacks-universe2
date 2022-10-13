# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function prod_db {
  local target="${1}"
  sops_export_vars 'observes/secrets/prod.yaml' \
    REDSHIFT_DATABASE \
    REDSHIFT_HOST \
    REDSHIFT_PORT \
    && jq -n \
      --arg n "${REDSHIFT_DATABASE}" \
      --arg h "${REDSHIFT_HOST}" \
      --arg p "${REDSHIFT_PORT}" \
      '{name: $n, host: $h, port: $p}' \
      > "${target}"
}

function prod_user {
  local target="${1}"
  sops_export_vars 'observes/secrets/prod.yaml' \
    REDSHIFT_USER \
    REDSHIFT_PASSWORD \
    && jq -n \
      --arg u "${REDSHIFT_USER}" \
      --arg p "${REDSHIFT_PASSWORD}" \
      '{user: $u, password: $p}' \
      > "${target}"
}

function json_db_creds {
  local target="${1}"
  sops_export_vars 'observes/secrets/prod.yaml' \
    REDSHIFT_DATABASE \
    REDSHIFT_HOST \
    REDSHIFT_PORT \
    REDSHIFT_USER \
    REDSHIFT_PASSWORD \
    && jq -n \
      --arg n "${REDSHIFT_DATABASE}" \
      --arg h "${REDSHIFT_HOST}" \
      --arg p "${REDSHIFT_PORT}" \
      --arg u "${REDSHIFT_USER}" \
      --arg pw "${REDSHIFT_PASSWORD}" \
      '{dbname: $n, host: $h, port: $p, user: $u, password: $pw}' \
      > "${target}"
}

function export_notifier_key {
  sops_export_vars 'observes/secrets/prod.yaml' \
    bugsnag_notifier_key
}
