# shellcheck shell=bash
alias scheduler="observes-service-jobs-scheduler-bin"

aws_login_prod_new 'observes' \
  && scheduler run-job "DYNAMO_INTEGRATES_MAIN"
