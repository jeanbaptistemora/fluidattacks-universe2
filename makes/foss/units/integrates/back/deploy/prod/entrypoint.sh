# shellcheck shell=bash

function hpa_replicas {
  local namespace="production"
  local name="integrates-master"
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

function main {
  export CI_COMMIT_REF_NAME='master'
  export B64_CI_COMMIT_REF_NAME
  export B64_CI_COMMIT_SHA
  export B64_PROD_INTEGRATES_AWS_ACCESS_KEY_ID
  export B64_PROD_INTEGRATES_AWS_SECRET_ACCESS_KEY
  export B64_PRODUCT_API_TOKEN
  export REPLICAS
  export UUID

  aws_login_prod_new integrates \
    && aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
    && B64_CI_COMMIT_REF_NAME="$(b64 "${CI_COMMIT_REF_NAME}")" \
    && B64_CI_COMMIT_SHA="$(b64 "${CI_COMMIT_SHA}")" \
    && B64_PROD_INTEGRATES_AWS_ACCESS_KEY_ID="$(b64 "${PROD_INTEGRATES_AWS_ACCESS_KEY_ID}")" \
    && B64_PROD_INTEGRATES_AWS_SECRET_ACCESS_KEY="$(b64 "${PROD_INTEGRATES_AWS_SECRET_ACCESS_KEY}")" \
    && B64_PRODUCT_API_TOKEN="$(b64 "${PRODUCT_API_TOKEN}")" \
    && REPLICAS="$(hpa_replicas)" \
    && UUID="$(uuidgen)" \
    && for manifest in __argManifests__/*; do
      echo "[INFO] Applying: ${manifest}" \
        && apply "${manifest}" \
        || return 1
    done \
    && echo '[INFO] Rolling out update' \
    && kubectl rollout status \
      "deploy/integrates-${CI_COMMIT_REF_NAME}" \
      -n 'production' \
      --timeout="30m" \
    && sops_export_vars integrates/secrets-production.yaml \
      CHECKLY_CHECK_ID \
      CHECKLY_TRIGGER_ID \
      NEW_RELIC_API_KEY \
      NEW_RELIC_APP_ID \
    && echo '[INFO] Announcing deployment to Checkly' \
    && curl "https://api.checklyhq.com/check-groups/${CHECKLY_CHECK_ID}/trigger/${CHECKLY_TRIGGER_ID}?deployment=true&repository=product/integrates&sha=${CI_COMMIT_SHA}" \
      --request 'GET' \
    && echo '[INFO] Announcing deployment to New Relic' \
    && curl "https://api.newrelic.com/v2/applications/${NEW_RELIC_APP_ID}/deployments.json" \
      --request 'POST' \
      --header "X-Api-Key: ${NEW_RELIC_API_KEY}" \
      --header 'Content-Type: application/json' \
      --include \
      --data "{
            \"deployment\": {
              \"revision\": \"${CI_COMMIT_SHA}\",
              \"user\": \"${CI_COMMIT_AUTHOR}\"
            }
          }"
}

main "${@}"
