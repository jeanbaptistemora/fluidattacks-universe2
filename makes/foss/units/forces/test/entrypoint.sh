# shellcheck shell=bash

function main {
  export INTEGRATES_FORCES_API_TOKEN
  export API_ENDPOINT

  local args_pytest=(
    --cov-branch
    --cov=forces
    --cov-fail-under '80'
    --cov-report 'term'
    --cov-report "html:${PWD}/forces/coverage/"
    --cov-report "xml:${PWD}/forces/coverage.xml"
    --disable-pytest-warnings
    --no-cov-on-fail
  )
  if ! test -z "${CI_COMMIT_REF_NAME:-}"; then
    API_ENDPOINT="https://${CI_COMMIT_REF_NAME}.app.fluidattacks.com/api"
  fi \
    && aws_login_dev_new \
    && if test -n "${CI:-}"; then
      aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "development" \
          --timeout="15m"
    fi \
    && sops_export_vars __argSecretsFile__ "INTEGRATES_FORCES_API_TOKEN" \
    && pushd forces/ \
    && source __argForcesRuntime__/template \
    && pytest "${args_pytest[@]}" \
    && popd || return 1
}

main "$@"
