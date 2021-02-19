# shellcheck shell=bash

function main {
  TF_VAR_aws_lambda_send_mail_notification_zip='__envLambdaSendMailNotification__' \
  integrates-infra-resources-test
}

main "${@}"
