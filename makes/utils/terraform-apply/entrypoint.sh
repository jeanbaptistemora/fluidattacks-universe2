# shellcheck shell=bash

function main {
      # Login with cloudflare if secrets provided
      if test -n '__envSecretsPath__'
      then
        cloudflare_login \
          'prod' \
          '__envProduct__' \
          '__envSecretsPath__'
      else
        aws_login_prod '__envProduct__'
      fi \
  &&  pushd '__envTarget__' \
    &&  echo '[INFO] Initializing' \
    &&  terraform init \
    &&  echo '[INFO] Applying changes' \
    &&  terraform apply -auto-approve -refresh=true "${@}" \
  &&  popd \
  ||  return 1
}

main "${@}"
