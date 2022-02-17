# shellcheck shell=bash
alias stability="observes-service-batch-stability-bin"

aws_login_prod 'observes' \
  && stability "${@}"
