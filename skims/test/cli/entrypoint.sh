# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function assert {
  if "${@}"; then
    info Successfully run: "${*}"
  else
    critical While running: "${*}"
  fi
}

function main {
  export INTEGRATES_API_ENDPOINT
  export INTEGRATES_API_TOKEN

  : \
    && aws_login "dev" "3600" \
    && sops_export_vars __argSecretsFile__ "INTEGRATES_API_TOKEN" \
    && if test -n "${CI:-}"; then
      aws_eks_update_kubeconfig 'common' 'us-east-1' \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "development" \
          --timeout="15m"
    fi \
    && if ! test -z "${CI_COMMIT_REF_NAME:-}"; then
      INTEGRATES_API_ENDPOINT="https://${CI_COMMIT_REF_NAME}.app.fluidattacks.com/api"
    else
      INTEGRATES_API_ENDPOINT="https://127.0.0.1:8001/api"
    fi
}

main "${@}"
