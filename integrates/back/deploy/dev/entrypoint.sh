# shellcheck shell=bash

function hpa_replicas {
  local namespace='development'
  local name="integrates-${CI_COMMIT_REF_NAME}"
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
  local target_product
  export B64_CI_COMMIT_REF_NAME
  export B64_CI_COMMIT_SHA
  export B64_DEV_AWS_ACCESS_KEY_ID
  export B64_DEV_AWS_SECRET_ACCESS_KEY
  export B64_GITLAB_USER_EMAIL
  export REPLICAS
  export UUID
  export DB_JOB

  aws_login_dev \
    && aws_eks_update_kubeconfig 'common' 'us-east-1' \
    && B64_CI_COMMIT_REF_NAME="$(b64 "${CI_COMMIT_REF_NAME}")" \
    && B64_CI_COMMIT_SHA="$(b64 "${CI_COMMIT_SHA}")" \
    && B64_DEV_AWS_ACCESS_KEY_ID="$(b64 "${DEV_AWS_ACCESS_KEY_ID}")" \
    && B64_DEV_AWS_SECRET_ACCESS_KEY="$(b64 "${DEV_AWS_SECRET_ACCESS_KEY}")" \
    && B64_GITLAB_USER_EMAIL="$(b64 "${GITLAB_USER_EMAIL}")" \
    && target_product="$(echo "${CI_COMMIT_TITLE}" | grep -oEi '^(airs|all|asserts|common|docs|forces|integrates|melts|observes|reviews|skims|sorts|teaches)')" \
    && if [ "${target_product}" = "integrates" ]; then
      DB_JOB="/integrates/db"
    else
      DB_JOB="/dynamoDb/${target_product}"
    fi \
    && REPLICAS="$(hpa_replicas)" \
    && UUID="$(uuidgen)" \
    && for manifest in __argManifests__/*; do
      echo "[INFO] Applying: ${manifest}" \
        && apply "${manifest}" \
        || return 1
    done
}

main "${@}"
