# shellcheck shell=bash
function main {
  shopt -s nullglob \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && pushd skims \
    && aws_login "prod_skims" "3600" \
    && python3 -m batch.__init__ "${@:2}" \
    && popd \
    || return 1
}

main "${@}"
