# shellcheck shell=bash

: \
  && aws_login "prod_sorts" "3600" \
  && sops_export_vars 'sorts/secrets.yaml' \
    'FERNET_TOKEN' \
    'MIXPANEL_API_TOKEN_SORTS' \
    'REDSHIFT_DATABASE' \
    'REDSHIFT_HOST' \
    'REDSHIFT_PASSWORD' \
    'REDSHIFT_PORT' \
    'REDSHIFT_USER'
sorts "${@}"
