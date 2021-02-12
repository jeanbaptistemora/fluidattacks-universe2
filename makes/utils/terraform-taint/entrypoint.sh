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
    &&  echo '[INFO] Refreshing state' \
    &&  terraform refresh \
    &&  for resource in "${@}"
        do
              echo "[INFO] Tainting ${resource}" \
          &&  terraform taint "${resource}" \
          ||  return 1
        done \
  &&  popd \
  ||  return 1
}

main "${@}"
