# shellcheck shell=bash

aws_login_prod 'sorts' \
  && sops_export_vars 'sorts/secrets.yaml' 'MIXPANEL_API_TOKEN_SORTS'
sorts "${@}"
