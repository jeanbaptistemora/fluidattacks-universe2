# shellcheck shell=bash

function resolve_endpoint() {
  if ! test -z "${CI_COMMIT_REF_NAME:-}"; then
    endpoint="https://${CI_COMMIT_REF_NAME}.app.fluidattacks.com/api"
  else
    endpoint="https://localhost:8001/api"
  fi
}

function main {
  local cluster="common-k8s"
  local region="us-east-1"
  export BATCH_BIN

  : \
    && aws_login "dev" "3600" \
    && if test -n "${CI:-}"; then
      aws_eks_update_kubeconfig "${cluster}" "${region}" \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "dev" \
          --timeout="15m"
    fi \
    && sops_export_vars __argIntegratesSecrets__/secrets/development.yaml \
      TEST_FORCES_TOKEN \
    && resolve_endpoint \
    && echo "[INFO] Running DevSecOps agent lax empty report check..." \
    && API_ENDPOINT="${endpoint}" forces --token "${TEST_FORCES_TOKEN}" --lax -v --repo-name universe \
    && echo "[INFO] Running DevSecOps agent strict check..." \
    && API_ENDPOINT="${endpoint}" forces --token "${TEST_FORCES_TOKEN}" --strict -vvvv --breaking 10.0 \
    || return 1
}

main "${@}"
