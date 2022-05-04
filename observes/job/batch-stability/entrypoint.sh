# shellcheck shell=bash
alias stability="observes-service-batch-stability-bin"

aws_login_prod 'observes' \
  && sops_export_vars 'observes/secrets/prod.yaml' \
    bugsnag_notifier_key \
  && stability "${@}"
