# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME
  export INTEGRATES_API_ENDPOINT

  sops_export_vars __argSecretsFile__ "INTEGRATES_API_TOKEN" \
    && if test '__argIsFunctionalTest__' = "1" && test -n "${CI:-}"; then
      aws_login_dev \
        && aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "development" \
          --timeout="15m"
    fi \
    && if ! test -z "${CI_COMMIT_REF_NAME:-}"; then
      INTEGRATES_API_ENDPOINT="https://${CI_COMMIT_REF_NAME}.app.fluidattacks.com/api"
    fi \
    && CI_COMMIT_REF_NAME="$(get_abbrev_rev "${PWD}" HEAD)"
}

main "${@}"
