# shellcheck shell=bash

aws_login_prod 'observes' \
  && sops_export_vars 'observes/secrets/prod.yaml' \
    bugsnag_notifier_key \
  && observes-scheduler run-job "DYNAMO_INTEGRATES_MAIN"
