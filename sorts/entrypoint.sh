# shellcheck shell=bash

: \
  && sops_export_vars 'sorts/secrets.yaml' \
    'MIXPANEL_API_TOKEN_SORTS' \
    'REDSHIFT_DATABASE' \
    'REDSHIFT_HOST' \
    'REDSHIFT_PASSWORD' \
    'REDSHIFT_PORT' \
    'REDSHIFT_USER'
sorts "${@}"
