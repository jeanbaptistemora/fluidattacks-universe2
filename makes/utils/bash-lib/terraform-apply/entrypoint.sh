#! __envShell__
# shellcheck shell=bash

source '__makeEntrypoint__'
source '__envUtilsBashLibAws__'

function main {
      aws_login_prod '__envProduct__' \
  &&  pushd '__envPath__' \
    &&  echo '[INFO] Initializing' \
    &&  '__envTerraform__' init \
    &&  echo '[INFO] Applying changes' \
    &&  '__envTerraform__' apply -auto-approve -refresh=true \
  &&  popd \
  ||  return 1
}

main "${@}"
