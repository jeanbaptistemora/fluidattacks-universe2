# shellcheck shell=bash

function skims_aws_login_dev {
  export AWS_ACCESS_KEY_ID
  export AWS_DEFAULT_REGION='us-east-1'
  export AWS_SECRET_ACCESS_KEY

      AWS_ACCESS_KEY_ID="${SKIMS_DEV_AWS_ACCESS_KEY_ID}" \
  &&  AWS_SECRET_ACCESS_KEY="${SKIMS_DEV_AWS_SECRET_ACCESS_KEY}" \
  &&  echo '[INFO] Logging into AWS with development credentials' \
  &&  '__envAwscli__' configure set 'aws_access_key_id' "${AWS_ACCESS_KEY_ID}" \
  &&  '__envAwscli__' configure set 'aws_secret_access_key' "${AWS_SECRET_ACCESS_KEY}"
}

function skims_aws_login_prod {
  export AWS_ACCESS_KEY_ID
  export AWS_DEFAULT_REGION='us-east-1'
  export AWS_SECRET_ACCESS_KEY

      AWS_ACCESS_KEY_ID="${SKIMS_PROD_AWS_ACCESS_KEY_ID}" \
  &&  AWS_SECRET_ACCESS_KEY="${SKIMS_PROD_AWS_SECRET_ACCESS_KEY}" \
  &&  echo '[INFO] Logging into AWS with production credentials' \
  &&  '__envAwscli__' configure set 'aws_access_key_id' "${AWS_ACCESS_KEY_ID}" \
  &&  '__envAwscli__' configure set 'aws_secret_access_key' "${AWS_SECRET_ACCESS_KEY}"
}

function skims_cache_pull {
  local flags=()
  local local="${1}"
  local remote="${2}"

      echo "[INFO] Moving skims state from ${remote} to ${local}" \
  &&  if test -n "${CI}"; then flags+=( --quiet ); fi \
  &&  '__envAwscli__' s3 sync "${flags[@]}" "${remote}" "${local}"
}

function skims_cache_push {
  local flags=()
  local local="${1}"
  local remote="${2}"

      echo "[INFO] Moving skims state from ${local} to ${remote}" \
  &&  if test -n "${CI}"; then flags+=( --quiet ); fi \
  &&  '__envAwscli__' s3 sync "${flags[@]}" "${local}" "${remote}"
}
