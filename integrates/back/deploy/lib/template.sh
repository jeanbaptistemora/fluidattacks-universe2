# shellcheck shell=bash

function is_int {
  local input="${1}"
  local regex="^[0-9]+$"

  if [[ ${input} =~ ${regex} ]]; then
    return 0
  else
    return 1
  fi
}

function hpa_desired_replicas {
  local name="${1}"
  local namespace="${2}"

  kubectl get hpa -n "${namespace}" -o yaml \
    | yq -r ".items[] | select(.metadata.name==\"${name}\") | .status.desiredReplicas"
}

function hpa_replicas {
  local namespace="dev"
  local name="integrates-${CI_COMMIT_REF_NAME}"
  local replicas

  : \
    && replicas="$(hpa_desired_replicas "${name}" "${namespace}")" \
    && if is_int "${replicas}" && test "${replicas}" != "0"; then
      echo "${replicas}"
    else
      echo 1
    fi
}

function apply_manifest {
  envsubst -no-unset -no-empty -i "${1}" | kubectl apply -f -
}

function b64 {
  echo -n "${1}" | base64 --wrap=0
}
