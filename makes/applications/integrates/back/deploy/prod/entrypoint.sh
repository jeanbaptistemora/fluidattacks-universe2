# shellcheck shell=bash

function apply {
  envsubst -no-unset -no-empty -i "${1}" | kubectl apply -f -
}

function b64 {
  echo -n "${1}" | base64 --wrap=0
}

function main {
  export CI_COMMIT_REF_NAME='master'
  export UUID
  export B64_CI_COMMIT_REF_NAME
  export B64_CI_COMMIT_SHA
  export B64_INTEGRATES_PROD_AWS_ACCESS_KEY_ID
  export B64_INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY

      aws_login_prod integrates \
  &&  aws_eks_update_kubeconfig 'integrates-cluster' 'us-east-1' \
  &&  B64_CI_COMMIT_REF_NAME="$(b64 "${CI_COMMIT_REF_NAME}")" \
  &&  B64_CI_COMMIT_SHA="$(b64 "${CI_COMMIT_SHA}")" \
  &&  B64_INTEGRATES_PROD_AWS_ACCESS_KEY_ID="$(b64 "${INTEGRATES_PROD_AWS_ACCESS_KEY_ID}")" \
  &&  B64_INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY="$(b64 "${INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY}")" \
  &&  UUID="$(uuidgen)" \
  &&  for manifest in __envManifests__/*
      do
            echo "[INFO] Applying: ${manifest}" \
        &&  apply "${manifest}" \
        ||  return 1
      done \
  &&  echo '[INFO] Rolling out update' \
  &&  kubectl rollout status \
        "deploy/integrates-${CI_COMMIT_REF_NAME}" \
        -n 'production' \
        --timeout="25m" \
  &&  sops_export_vars integrates/secrets-production.yaml \
        CHECKLY_CHECK_ID \
        CHECKLY_TRIGGER_ID \
        NEW_RELIC_API_KEY \
        NEW_RELIC_APP_ID \
  &&  echo '[INFO] Announcing deployment to Checkly' \
  &&  curl "https://api.checklyhq.com/check-groups/${CHECKLY_CHECK_ID}/trigger/${CHECKLY_TRIGGER_ID}?deployment=true&repository=product/integrates&sha=${CI_COMMIT_SHA}" \
        --request 'GET' \
  &&  echo '[INFO] Announcing deployment to New Relic' \
  &&  curl "https://api.newrelic.com/v2/applications/${NEW_RELIC_APP_ID}/deployments.json" \
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
