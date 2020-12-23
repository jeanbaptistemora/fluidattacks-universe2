# shellcheck shell=bash

function aws_login_dev {
  local key="${1^^}_DEV_AWS_ACCESS_KEY_ID"
  local secret="${1^^}_DEV_AWS_SECRET_ACCESS_KEY"
  export AWS_ACCESS_KEY_ID="${!key}"
  export AWS_DEFAULT_REGION='us-east-1'
  export AWS_SECRET_ACCESS_KEY="${!secret}"

      echo '[INFO] Logging into AWS with development credentials' \
  &&  '__envAwscli__' configure set 'aws_access_key_id' "${AWS_ACCESS_KEY_ID}" \
  &&  '__envAwscli__' configure set 'aws_secret_access_key' "${AWS_SECRET_ACCESS_KEY}"
}

function aws_login_prod {
  local key="${1^^}_PROD_AWS_ACCESS_KEY_ID"
  local secret="${1^^}_PROD_AWS_SECRET_ACCESS_KEY"
  export AWS_ACCESS_KEY_ID="${!key}"
  export AWS_DEFAULT_REGION='us-east-1'
  export AWS_SECRET_ACCESS_KEY="${!secret}"

      echo '[INFO] Logging into AWS with production credentials' \
  &&  '__envAwscli__' configure set 'aws_access_key_id' "${AWS_ACCESS_KEY_ID}" \
  &&  '__envAwscli__' configure set 'aws_secret_access_key' "${AWS_SECRET_ACCESS_KEY}"
}

function aws_s3_sync {
  local flags=()
  local from="${1}"
  local to="${2}"

      echo "[INFO] Syncing data to AWS from ${from} to ${to}" \
  &&  if test -n "${CI}"; then flags+=( --quiet ); fi \
  &&  '__envAwscli__' s3 sync "${flags[@]}" "${from}" "${to}"
}
