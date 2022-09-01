# shellcheck shell=bash

function hpa_replicas {
  local namespace="production"
  local name="integrates-trunk"
  local replicas

  function hpa_desired_replicas {
    kubectl get hpa -n "${namespace}" -o yaml \
      | yq -r ".items[] | select(.metadata.name==\"${name}\") | .status.desiredReplicas"
  }

  function is_int {
    local input="${1}"
    local regex="^[0-9]+$"

    if [[ ${input} =~ ${regex} ]]; then
      return 0
    else
      return 1
    fi
  }

  replicas="$(hpa_desired_replicas)" \
    && if is_int "${replicas}" && test "${replicas}" != "0"; then
      echo "${replicas}"
    else
      echo 1
    fi
}

function apply {
  envsubst -no-unset -no-empty -i "${1}" | kubectl apply -f -
}

function b64 {
  echo -n "${1}" | base64 --wrap=0
}

function report_deployment_checkly {
  echo '[INFO] Announcing deployment to Checkly' \
    && curl "https://api.checklyhq.com/check-groups/${CHECKLY_CHECK_ID}/trigger/${CHECKLY_TRIGGER_ID}?deployment=true&repository=product/integrates&sha=${CI_COMMIT_SHA}" \
      --request 'GET'
}

function report_deployment {
  report_deployment_checkly
}

function rollout {
  local name="${1}"

  echo '[INFO] Rolling out update' \
    && kubectl rollout status \
      "deploy/integrates-${name}" \
      -n 'production' \
      --timeout="30m"
}

function deploy {
  local name="${1}"
  local endpoint="${2}"
  export NAME="${name}"
  export ENDPOINT="${endpoint}"
  export B64_CACHIX_AUTH_TOKEN
  export CI_COMMIT_REF_NAME='trunk'
  export B64_CI_COMMIT_REF_NAME
  export B64_CI_COMMIT_SHA
  export B64_UNIVERSE_API_TOKEN
  export REPLICAS
  export UUID

  : \
    && aws_login "prod_integrates" "3600" \
    && aws_eks_update_kubeconfig 'common' 'us-east-1' \
    && B64_CACHIX_AUTH_TOKEN="$(b64 "${CACHIX_AUTH_TOKEN}")" \
    && B64_CI_COMMIT_REF_NAME="$(b64 "${CI_COMMIT_REF_NAME}")" \
    && B64_CI_COMMIT_SHA="$(b64 "${CI_COMMIT_SHA}")" \
    && B64_UNIVERSE_API_TOKEN="$(b64 "${UNIVERSE_API_TOKEN}")" \
    && REPLICAS="$(hpa_replicas)" \
    && UUID="$(uuidgen)" \
    && sops_export_vars integrates/secrets/production.yaml \
      CHECKLY_CHECK_ID \
      CHECKLY_TRIGGER_ID \
    && for manifest in __argManifests__/*; do
      echo "[INFO] Applying: ${manifest}" \
        && apply "${manifest}" \
        || return 1
    done
}

function main {
  deploy "trunk" "app" \
    && rollout "trunk" \
    && report_deployment
}

main "${@}"
