# shellcheck shell=bash

: \
  && aws_login "prod_sorts" "3600" \
  && sops_export_vars 'sorts/secrets.yaml' \
    REDSHIFT_USER \
    REDSHIFT_PASSWORD \
    REDSHIFT_DATABASE \
    REDSHIFT_HOST \
    REDSHIFT_PORT \
  && association-rules "${@}"
