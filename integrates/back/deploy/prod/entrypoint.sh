# shellcheck shell=bash

function deploy {
  local cluster="common-k8s"
  local region="us-east-1"
  local name="${1}"
  local endpoint="${2}"
  export NAME="${name}"
  export ENDPOINT="${endpoint}"
  export B64_CACHIX_AUTH_TOKEN
  export CI_COMMIT_REF_NAME='trunk'
  export B64_CI_COMMIT_REF_NAME
  export B64_CI_COMMIT_SHA
  export B64_UNIVERSE_API_TOKEN
  export UUID

  : \
    && aws_login "prod_integrates" "3600" \
    && aws_eks_update_kubeconfig "${cluster}" "${region}" \
    && B64_CACHIX_AUTH_TOKEN="$(b64 "${CACHIX_AUTH_TOKEN}")" \
    && B64_CI_COMMIT_REF_NAME="$(b64 "${CI_COMMIT_REF_NAME}")" \
    && B64_CI_COMMIT_SHA="$(b64 "${CI_COMMIT_SHA}")" \
    && B64_UNIVERSE_API_TOKEN="$(b64 "${UNIVERSE_API_TOKEN}")" \
    && UUID="$(uuidgen)" \
    && sops_export_vars integrates/secrets/production.yaml \
      CHECKLY_CHECK_ID \
      CHECKLY_TRIGGER_ID \
    && for manifest in __argManifests__/*; do
      apply_manifest "${manifest}"
    done
}

function main {
  deploy "trunk" "app" \
    && rollout "integrates-trunk" "prod-integrates" \
    && report_deployment "product/integrates"
}

main "${@}"
