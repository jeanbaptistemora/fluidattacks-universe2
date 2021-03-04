# shellcheck shell=bash

function apply {
  envsubst -no-unset -no-empty -i "${1}" | kubectl apply -f -
}

function b64 {
  echo -n "${1}" | base64 --wrap=0
}

function main {
  export UUID
  export B64_CI_COMMIT_REF_NAME
  export B64_CI_COMMIT_SHA
  export B64_INTEGRATES_DEV_AWS_ACCESS_KEY_ID
  export B64_INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY

      aws_login_dev integrates \
  &&  aws_eks_update_kubeconfig 'integrates-cluster' 'us-east-1' \
  &&  B64_CI_COMMIT_REF_NAME="$(b64 "${CI_COMMIT_REF_NAME}")" \
  &&  B64_CI_COMMIT_SHA="$(b64 "${CI_COMMIT_SHA}")" \
  &&  B64_INTEGRATES_DEV_AWS_ACCESS_KEY_ID="$(b64 "${INTEGRATES_DEV_AWS_ACCESS_KEY_ID}")" \
  &&  B64_INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY="$(b64 "${INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY}")" \
  &&  UUID="$(uuidgen)" \
  &&  for manifest in __envManifests__/*
      do
            echo "[INFO] Applying: ${manifest}" \
        &&  apply "${manifest}" \
        ||  return 1
      done
}

main "${@}"
