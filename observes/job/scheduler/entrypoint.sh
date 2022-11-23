# shellcheck shell=bash

: \
  && aws_login "prod_observes" "3600" \
  && export AWS_DEFAULT_REGION="us-east-1" \
  && sops_export_vars 'observes/secrets/prod.yaml' \
    bugsnag_notifier_key \
  && observes-scheduler run-schedule
