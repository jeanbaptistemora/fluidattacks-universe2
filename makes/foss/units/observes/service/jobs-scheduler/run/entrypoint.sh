# shellcheck shell=bash
alias scheduler="observes-service-jobs-scheduler-bin"

aws_login_prod 'observes' \
  && scheduler run-job "DYNAMO_INTEGRATES_MAIN"
