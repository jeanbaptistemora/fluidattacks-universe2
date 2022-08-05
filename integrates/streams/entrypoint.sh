# shellcheck shell=bash
function export_secrets {
  local env="${1}"
  local secrets=(
    AWS_OPENSEARCH_HOST
    DYNAMODB_HOST
    DYNAMODB_PORT
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
    && pushd integrates/streams/src \
    && python3 "invoker.py" "${module}" \
    && popd \
    || return 1
}

main "${@}"
