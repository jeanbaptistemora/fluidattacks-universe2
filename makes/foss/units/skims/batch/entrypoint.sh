# shellcheck shell=bash
function main {
  shopt -s nullglob \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
      PROD_SERVICES_AWS_ACCESS_KEY_ID \
      PROD_SERVICES_AWS_SECRET_ACCESS_KEY \
    && pushd skims \
    && aws_login_prod 'skims' \
    && python3 -m batch.__init__ "${@:2}" \
    && popd \
    || return 1
}

main "${@}"
