# shellcheck shell=bash

: \
  && sops_export_vars 'sorts/secrets.yaml' \
    REDSHIFT_USER \
    REDSHIFT_PASSWORD \
    REDSHIFT_DATABASE \
    REDSHIFT_HOST \
    REDSHIFT_PORT \
  && association-rules "${@}"
