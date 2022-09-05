# shellcheck shell=bash

function associate {
  local group="${1}"
  local success

  { clone_services_repository "${group}" || true; } \
    && if ! test -e "groups/${group}/fusion"; then
      echo '[WARNING] No repositories to test' \
        && return 0
    fi \
    && echo '[INFO] Running sorts:' \
    && if sorts --association-rules "groups/${group}"; then
      echo "[INFO] Succesfully executed on: ${group}" \
        && success='true'
    else
      echo "[ERROR] While running Sorts on: ${group}" \
        && success='false'
    fi \
    && rm -rf "groups/${group}/fusion" \
    && test "${success}" = 'true'
}

function main {
  local parallel="${1}"
  local groups_file

  : \
    && aws_login "prod_sorts" "3600" \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && sops_export_vars 'sorts/secrets.yaml' \
      'MIXPANEL_API_TOKEN_SORTS' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && use_git_repo_services \
    && groups_file="$(mktemp)" \
    && ls -1 groups > "${groups_file}" \
    && execute_chunk_parallel associate "${groups_file}" "${parallel}" "batch"

}

main "${@}"
