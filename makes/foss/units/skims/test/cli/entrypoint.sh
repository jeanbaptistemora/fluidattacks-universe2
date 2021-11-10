# shellcheck shell=bash

function assert {
  if "${@}"; then
    info Successfully run: "${*}"
  else
    critical While running: "${*}"
  fi
}

function main {
  local output
  export INTEGRATES_API_ENDPOINT
  export INTEGRATES_API_TOKEN

  sops_export_vars __argSecretsFile__ "INTEGRATES_API_TOKEN" \
    && if test -n "${CI:-}"; then
      aws_login_dev_new \
        && aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "development" \
          --timeout="15m"
    fi \
    && if ! test -z "${CI_COMMIT_REF_NAME:-}"; then
      INTEGRATES_API_ENDPOINT="https://${CI_COMMIT_REF_NAME}.app.fluidattacks.com/api"
    else
      INTEGRATES_API_ENDPOINT="https://127.0.0.1:8001/api"
    fi \
    && output="$(mktemp)" \
    && assert skims expected-code-date --finding-code F117 --group jessup --namespace services |& tee "${output}" \
    && assert grep -HnP '^(0|1622\d+)$' "${output}" \
    && assert grep -HnP 'Success' "${output}" \
    && assert skims language --group jessup |& tee "${output}" \
    && assert grep -HnP '^EN$' "${output}" \
    && assert grep -HnP 'Success' "${output}"
}

main "${@}"
