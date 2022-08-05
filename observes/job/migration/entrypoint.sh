# shellcheck shell=bash

export SOURCE_DB_USER
export SOURCE_DB_PASSWORD
export SOURCE_DB_NAME
export SOURCE_DB_HOST
export SOURCE_DB_PORT

export TARGET_DB_USER
export TARGET_DB_PASSWORD
export TARGET_DB_NAME
export TARGET_DB_HOST
export TARGET_DB_PORT

: \
  && sops_export_vars 'observes/secrets/prod.yaml' \
    REDSHIFT_OLD_USER \
    REDSHIFT_OLD_PASSWORD \
    REDSHIFT_OLD_DATABASE \
    REDSHIFT_OLD_HOST \
    REDSHIFT_OLD_PORT \
    REDSHIFT_USER \
    REDSHIFT_PASSWORD \
    REDSHIFT_DATABASE \
    REDSHIFT_HOST \
    REDSHIFT_PORT \
    bugsnag_notifier_key \
  && SOURCE_DB_USER="${REDSHIFT_OLD_USER}" \
  && SOURCE_DB_PASSWORD="${REDSHIFT_OLD_PASSWORD}" \
  && SOURCE_DB_NAME="${REDSHIFT_OLD_DATABASE}" \
  && SOURCE_DB_HOST="${REDSHIFT_OLD_HOST}" \
  && SOURCE_DB_PORT="${REDSHIFT_OLD_PORT}" \
  && TARGET_DB_USER="${REDSHIFT_USER}" \
  && TARGET_DB_PASSWORD="${REDSHIFT_PASSWORD}" \
  && TARGET_DB_NAME="${REDSHIFT_DATABASE}" \
  && TARGET_DB_HOST="${REDSHIFT_HOST}" \
  && TARGET_DB_PORT="${REDSHIFT_PORT}" \
  && python -m db_migration
