# shellcheck shell=bash

source '__envSearchPaths__'
source '__envUtilsCloudflare__'

function main {
      cloudflare_login \
        'prod' \
        '__envProduct__' \
        '__envSecretsPath__' \
  &&  pushd '__envTarget__' \
    &&  echo '[INFO] Initializing' \
    &&  terraform init \
    &&  echo '[INFO] Applying changes' \
    &&  terraform apply -auto-approve -refresh=true "${@}" \
  &&  popd \
  ||  return 1
}

main "${@}"
