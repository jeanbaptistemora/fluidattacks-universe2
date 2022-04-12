# shellcheck shell=bash

function resolve_endpoint() {
  if ! test -z "${CI_COMMIT_REF_NAME:-}"; then
    endpoint="https://${CI_COMMIT_REF_NAME}.app.fluidattacks.com/api"
  else
    endpoint="https://localhost:8001/api"
  fi
}

function check_output() {
  if ! grep -q "ERROR\|TypeError\|IndexError\|Traceback" "$1"; then
    echo "[INFO] All clear!"
    result_code=0
  else
    echo "[ERROR] Failed check"
    grep -q "ERROR\|TypeError\|IndexError\|Traceback" "$1"
    result_code=1
  fi
}

function main {
  local out="out"
  export BATCH_BIN

  aws_login_dev \
    && if test -n "${CI:-}"; then
      aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "development" \
          --timeout="15m"
    fi \
    && sops_export_vars __argIntegratesSecrets__/secrets-development.yaml \
      TEST_FORCES_TOKEN \
    && resolve_endpoint \
    && echo "[INFO] Running DevSecOps agent check..." \
    && mkdir -p "${out}" \
    && API_ENDPOINT="${endpoint}" forces --token "${TEST_FORCES_TOKEN}" --lax > "${out}/forces-output.log" || true \
    && check_output "${out}/forces-output.log" \
    && rm -rf "${out}" \
    && API_ENDPOINT="${endpoint}" forces --token "${TEST_FORCES_TOKEN}" --lax \
    && ! (($? | "${result_code}")) \
    || return 1
}

main "${@}"
