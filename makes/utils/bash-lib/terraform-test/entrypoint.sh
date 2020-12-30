#! __envShell__
# shellcheck shell=bash

source '__makeEntrypoint__'
source '__envUtilsBashLibAws__'

function main {
      aws_login_dev '__envProduct__' \
  &&  pushd '__envPath__' \
    &&  echo '[INFO] Initializing' \
    &&  '__envTerraform__' init \
    &&  echo '[INFO] Running tflint' \
    &&  '__envTflint__' -c '__envTflintConfig__' \
    &&  echo '[INFO] Planning' \
    &&  '__envTerraform__' plan -lock=false -refresh=true \
  &&  popd \
  ||  return 1
}

main "${@}"
