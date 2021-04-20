# shellcheck shell=bash

function main {
  # Try to export okta and cloudflare vars if secrets provided
      aws_login_dev '__envProduct__' \
  &&  if test -n '__envSecretsPath__'
      then
        sops_export_vars_terraform \
          '__envSecretsPath__' \
          '(OKTA|CLOUDFLARE)'
      fi \
  &&  pushd '__envTarget__' \
    &&  echo '[INFO] Initializing' \
    &&  terraform init \
    &&  echo '[INFO] Checking format' \
    &&  if ! terraform fmt -check -list=false -recursive
        then
              echo '[ERROR] Source code is not formated with: terraform fmt' \
          &&  echo '[INFO] We will format it for you, but the job will fail' \
          &&  terraform fmt -list=false -recursive \
          &&  return 1 \
          ||  return 1
        fi \
    &&  echo '[INFO] Running tflint' \
    &&  tflint -c '__envTflintConfig__' \
    &&  echo '[INFO] Planning' \
    &&  terraform plan -lock=false -refresh=true "${@}" \
  &&  popd \
  ||  return 1
}

main "${@}"
