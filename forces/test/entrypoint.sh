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
    --verbose
  )
  aws_login "dev" "3600" \
    && if test -n "${CI:-}"; then
      aws_eks_update_kubeconfig 'common' 'us-east-1' \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "dev" \
          --timeout="15m"
    fi \
    && sops_export_vars __argSecretsFile__ "TEST_FORCES_TOKEN" \
    && pushd forces/ \
    && source __argForcesRuntime__/template \
    && pytest "${args_pytest[@]}" \
    && popd || return 1
}

main "$@"
