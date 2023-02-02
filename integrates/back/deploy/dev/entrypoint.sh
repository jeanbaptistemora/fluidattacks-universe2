# shellcheck shell=bash

function main {
  local cluster="common-k8s"
  local region="us-east-1"
  local target_product
  export B64_CACHIX_AUTH_TOKEN
  export B64_CI_COMMIT_REF_NAME
  export B64_CI_COMMIT_SHA
  export B64_GITLAB_USER_EMAIL
  export REPLICAS
  export UUID
  export DB_JOB

  : \
    && aws_login "dev" "3600" \
    && aws_eks_update_kubeconfig "${cluster}" "${region}" \
    && B64_CACHIX_AUTH_TOKEN="$(b64 "${CACHIX_AUTH_TOKEN}")" \
    && B64_CI_COMMIT_REF_NAME="$(b64 "${CI_COMMIT_REF_NAME}")" \
    && B64_CI_COMMIT_SHA="$(b64 "${CI_COMMIT_SHA}")" \
    && B64_GITLAB_USER_EMAIL="$(b64 "${GITLAB_USER_EMAIL}")" \
    && target_product="$(echo "${CI_COMMIT_TITLE}" | grep -oEi '^(airs|all|asserts|common|docs|forces|integrates|melts|observes|reviews|skims|sorts|teaches)')" \
    && if [ "${target_product}" = "integrates" ]; then
      DB_JOB="/integrates/db"
    else
      DB_JOB="/dynamoDb/${target_product}"
    fi \
    && REPLICAS="$(hpa_replicas "integrates-${CI_COMMIT_REF_NAME}" "dev")" \
    && UUID="$(uuidgen)" \
    && for manifest in __argManifests__/*; do
      apply_manifest "${manifest}"
    done
}

main "${@}"
