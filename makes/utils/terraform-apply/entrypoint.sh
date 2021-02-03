# shellcheck shell=bash

source '__envSearchPaths__'
source '__envUtilsBashLibAws__'

function main {
      aws_login_prod '__envProduct__' \
  &&  pushd '__envTarget__' \
    &&  echo '[INFO] Initializing' \
    &&  terraform init \
    &&  echo '[INFO] Applying changes' \
    &&  terraform apply -auto-approve -refresh=true "${@}" \
  &&  popd \
  ||  return 1
}

main "${@}"
