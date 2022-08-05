# shellcheck shell=bash
function main {
  shopt -s nullglob \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && pushd skims \
    && aws_login_prod 'skims' \
    && sops_export_vars __argSecretsProd__ "DYNAMODB_HOST" "DYNAMODB_PORT" "ENVIRONMENT" \
    && python3 -m batch.__init__ "${@:2}" \
    && popd \
    || return 1
}

main "${@}"
