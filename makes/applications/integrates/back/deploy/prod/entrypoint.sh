# shellcheck shell=bash

function hpa_replicas {
  local namespace='production'
  local name="integrates-master"
  local hpas

  function hpa_desired_replicas {
    echo "${hpas}" \
      | yq -er ".items[] | select(.metadata.name==\"${name}\") | .status.desiredReplicas"
  }

  hpas=$(kubectl get hpa -n "${namespace}" -o yaml) \
    && if hpa_desired_replicas > /dev/null; then
      hpa_desired_replicas
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
  export B64_INTEGRATES_PROD_AWS_ACCESS_KEY_ID
  export B64_INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY
  export B64_PRODUCT_API_TOKEN
  export REPLICAS
  export UUID

  aws_login_prod integrates \
    && aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
    && B64_CI_COMMIT_REF_NAME="$(b64 "${CI_COMMIT_REF_NAME}")" \
    && B64_CI_COMMIT_SHA="$(b64 "${CI_COMMIT_SHA}")" \
    && B64_INTEGRATES_PROD_AWS_ACCESS_KEY_ID="$(b64 "${INTEGRATES_PROD_AWS_ACCESS_KEY_ID}")" \
    && B64_INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY="$(b64 "${INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY}")" \
    && B64_PRODUCT_API_TOKEN="$(b64 "${PRODUCT_API_TOKEN}")" \
    && REPLICAS="$(hpa_replicas)" \
    && UUID="$(uuidgen)" \
    && for manifest in __envManifests__/*; do
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
