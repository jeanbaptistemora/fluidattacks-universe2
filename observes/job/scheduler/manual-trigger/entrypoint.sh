# shellcheck shell=bash

: \
  && source "__argSecretsAwsProd__/template" \
  && sops_export_vars 'observes/secrets/prod.yaml' \
    bugsnag_notifier_key \
  && observes-scheduler run-job "UPLOAD"
