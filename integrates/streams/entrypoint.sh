# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash
function export_secrets {
  local env="${1}"
  local secrets=(
    AWS_OPENSEARCH_HOST
    AWS_REDSHIFT_DBNAME
    AWS_REDSHIFT_HOST
    AWS_REDSHIFT_PASSWORD
    AWS_REDSHIFT_USER
    DYNAMODB_HOST
    DYNAMODB_PORT
    GOOGLE_CHAT_WEBOOK_URL
  )
  local secrets_path

  case "${env}" in
    dev) secrets_path=__argSecretsDev__ ;;
    prod-local) secrets_path=__argSecretsDev__ ;;
    prod) secrets_path=__argSecretsProd__ ;;
    *) error 'First argument must be one of: dev, prod, prod-local' ;;
  esac \
    && sops_export_vars "${secrets_path}" "${secrets[@]}" \
    || return 1
}

function main {
  export ENVIRONMENT="${1}"
  local module="${2}"
  export AWS_DEFAULT_REGION="us-east-1"

  echo "[INFO] Executing ${module} consumer" \
    && export_secrets "${ENVIRONMENT}" \
    && pushd __argSrc__ \
    && python3 "invoker.py" "${module}" \
    && popd \
    || return 1
}

main "${@}"
