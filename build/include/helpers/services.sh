# shellcheck shell=bash

function helper_services_aws_login {
  local user="${1}"
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY


      if [ "${user}" = 'dev' ]
      then
            AWS_ACCESS_KEY_ID="${SERVICES_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SERVICES_DEV_AWS_SECRET_ACCESS_KEY}"
      elif [ "${user}" = 'prod' ]
      then
            AWS_ACCESS_KEY_ID="${SERVICES_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SERVICES_PROD_AWS_SECRET_ACCESS_KEY}"
      else
            echo '[ERROR] either prod or dev must be passed as arg' \
        &&  return 1
      fi \
  &&  echo "[INFO] Logging into services AWS with ${user} credentials" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}
