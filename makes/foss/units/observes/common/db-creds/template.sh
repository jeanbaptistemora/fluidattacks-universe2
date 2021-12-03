# shellcheck shell=bash

function prod_db {
  local target="${1}"
  sops_export_vars 'observes/secrets-prod.yaml' \
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
  sops_export_vars 'observes/secrets-prod.yaml' \
    REDSHIFT_USER \
    REDSHIFT_PASSWORD \
    && jq -n \
      --arg u "${REDSHIFT_USER}" \
      --arg p "${REDSHIFT_PASSWORD}" \
      '{user: $u, password: $p}' \
      > "${target}"
}
