# shellcheck shell=bash

: \
  && source "__argSecretsAwsProd__/template" \
  && export AWS_DEFAULT_REGION="us-east-1" \
  && sops_export_vars 'observes/secrets/prod.yaml' \
    bugsnag_notifier_key \
  && observes-scheduler run-schedule
