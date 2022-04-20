# shellcheck shell=bash
alias scheduler="observes-service-jobs-scheduler-bin"

aws_login_prod 'observes' \
  && scheduler run-job "MIRROR" \
  && scheduler run-job "ANNOUNCEKIT" \
  && scheduler run-job "BUGSNAG" \
  && scheduler run-job "CHECKLY" \
  && scheduler run-job "DELIGHTED"
