# shellcheck shell=bash

function resolve_endpoint() {
  if ! test -z "${CI_COMMIT_REF_NAME:-}"; then
    API_ENDPOINT="https://${CI_COMMIT_REF_NAME}.app.fluidattacks.com/api"
  else
    API_ENDPOINT="https://localhost:8001/api"
  fi
}

function main {
  aws_login_dev \
    && if test -n "${CI:-}"; then
      aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "development" \
          --timeout="15m"
    fi \
    && resolve_endpoint \
    && NODE_TLS_REJECT_UNAUTHORIZED='0' \
      graphql-inspector diff \
      https://app.fluidattacks.com/api \
      ${API_ENDPOINT} \
      --rule suppressRemovalOfDeprecatedField
}

main "${@}"
