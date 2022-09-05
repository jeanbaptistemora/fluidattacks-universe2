# shellcheck shell=bash

: \
  && aws_login "prod_observes" "3600" \
  && sops_export_vars 'observes/secrets/prod.yaml' \
    bugsnag_notifier_key \
  && observes-batch-stability "${@}"
