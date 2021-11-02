# shellcheck shell=bash

function hpa_replicas {
  local namespace='development'
  local name="integrates-${CI_COMMIT_REF_NAME}"
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
  export B64_CI_COMMIT_REF_NAME
  export B64_CI_COMMIT_SHA
  export B64_DEV_AWS_ACCESS_KEY_ID
  export B64_DEV_AWS_SECRET_ACCESS_KEY
  export REPLICAS
  export UUID

  aws_login_dev_new \
    && aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
    && B64_CI_COMMIT_REF_NAME="$(b64 "${CI_COMMIT_REF_NAME}")" \
    && B64_CI_COMMIT_SHA="$(b64 "${CI_COMMIT_SHA}")" \
    && B64_DEV_AWS_ACCESS_KEY_ID="$(b64 "${DEV_AWS_ACCESS_KEY_ID}")" \
    && B64_DEV_AWS_SECRET_ACCESS_KEY="$(b64 "${DEV_AWS_SECRET_ACCESS_KEY}")" \
    && REPLICAS="$(hpa_replicas)" \
    && UUID="$(uuidgen)" \
    && for manifest in __argManifests__/*; do
      echo "[INFO] Applying: ${manifest}" \
        && apply "${manifest}" \
        || return 1
    done
}

main "${@}"
