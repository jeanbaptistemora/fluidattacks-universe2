# shellcheck shell=bash

source '__envUtilsBashLibAws__'

function main {
      aws_login_dev '__envProduct__' \
  &&  pushd '__envPath__' \
    &&  echo '[INFO] Initializing' \
    &&  '__envTerraform__' init \
    &&  echo '[INFO] Checking format' \
    &&  if ! '__envTerraform__' fmt -check -list=false -recursive
        then
              echo '[ERROR] Source code is not formated with: terraform fmt' \
          &&  echo '[INFO] We will format it for you, but the job will fail' \
          &&  terraform fmt -list=false -recursive \
          &&  return 1 \
          ||  return 1
        fi \
    &&  echo '[INFO] Running tflint' \
    &&  '__envTflint__' -c '__envTflintConfig__' \
    &&  echo '[INFO] Planning' \
    &&  '__envTerraform__' plan -lock=false -refresh=true \
  &&  popd \
  ||  return 1
}

main "${@}"
