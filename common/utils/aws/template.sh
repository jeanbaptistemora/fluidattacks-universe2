# shellcheck shell=bash

function _get_credential {
  local credential="${1}"
  local session="${2}"

  echo "${session}" | jq -rec ".Credentials.${credential}"
}

function _aws_login_ci {
  local args=(
    --role-arn "arn:aws:iam::205810638802:role/${1}"
    --role-session-name "commonCi-${CI_PROJECT_ID}-${CI_PIPELINE_ID}-${CI_JOB_ID}"
    --web-identity-token "${CI_JOB_JWT_V2}"
    --duration-seconds "${2:-3600}"
  )
  local session
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_SESSION_TOKEN

  : \
    && session="$(aws sts assume-role-with-web-identity "${args[@]}")" \
    && AWS_ACCESS_KEY_ID="$(_get_credential "AccessKeyId" "${session}")" \
    && AWS_SECRET_ACCESS_KEY="$(_get_credential "SecretAccessKey" "${session}")" \
    && AWS_SESSION_TOKEN="$(_get_credential "SessionToken" "${session}")"
}

function aws_login {
  local session="${1}"
  local duration="${2}"

  if test -n "${CI_JOB_JWT_V2:-}"; then
    info "Logging in as '${session}' using GitLab OIDC." \
      && _aws_login_ci "${session}" "${duration}"
  else
    info "Looks like this job is not running on GitLab CI. Skipping."
  fi
}

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
  local key="PROD_${1^^}_AWS_ACCESS_KEY_ID"
  local secret="PROD_${1^^}_AWS_SECRET_ACCESS_KEY"
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
