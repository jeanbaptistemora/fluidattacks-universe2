# shellcheck shell=bash

function aws_login_dev {
  local key="DEV_AWS_ACCESS_KEY_ID"
  local secret="DEV_AWS_SECRET_ACCESS_KEY"
  export AWS_ACCESS_KEY_ID
  export AWS_DEFAULT_REGION='us-east-1'
  export AWS_SECRET_ACCESS_KEY
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

  echo '[INFO] Logging into AWS with development credentials' \
    && ensure_gitlab_env_vars "${key}" "${secret}" \
    && AWS_ACCESS_KEY_ID="${!key}" \
    && AWS_SECRET_ACCESS_KEY="${!secret}" \
    && aws configure set 'aws_access_key_id' "${AWS_ACCESS_KEY_ID}" \
    && aws configure set 'aws_secret_access_key' "${AWS_SECRET_ACCESS_KEY}" \
    && TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}" \
    && TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}"
}

function aws_login_prod {
  local key="${1^^}_PROD_AWS_ACCESS_KEY_ID"
  local secret="${1^^}_PROD_AWS_SECRET_ACCESS_KEY"
  export AWS_ACCESS_KEY_ID
  export AWS_DEFAULT_REGION='us-east-1'
  export AWS_SECRET_ACCESS_KEY
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

  echo '[INFO] Logging into AWS with production credentials' \
    && ensure_gitlab_env_vars "${key}" "${secret}" \
    && AWS_ACCESS_KEY_ID="${!key}" \
    && AWS_SECRET_ACCESS_KEY="${!secret}" \
    && aws configure set 'aws_access_key_id' "${AWS_ACCESS_KEY_ID}" \
    && aws configure set 'aws_secret_access_key' "${AWS_SECRET_ACCESS_KEY}" \
    && TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}" \
    && TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}"
}

function aws_s3_sync {
  local flags=(
    --follow-symlinks
  )
  local from="${1}"
  local to="${2}"

  echo "[INFO] Syncing AWS S3 data from ${from} to ${to}" \
    && if test -n "${CI:-}"; then flags+=(--quiet); fi \
    && aws s3 sync "${@:3}" "${flags[@]}" "${from}" "${to}"
}

function aws_eks_update_kubeconfig {
  local name="${1}"
  local region="${2}"

  aws eks update-kubeconfig --name "${name}" --region "${region}"
}
