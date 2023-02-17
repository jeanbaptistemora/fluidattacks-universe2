# shellcheck shell=bash

function execute {
  local group="${1}"
  local success

  for i in {1..10}; do
    if clone_services_repository "${group}"; then
      break
    else
      echo "[WARNING] Try #${i} for pulling repo of group ${group} has failed"
      sleep 10
    fi
  done
  if ! test -e "groups/${group}/fusion"; then
    echo '[WARNING] No repositories to test' \
      && return 0
  fi \
    && echo "[INFO] Running sorts on group ${group}:" \
    && if sorts "groups/${group}"; then
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
  local sorted_groups_file

  : \
    && aws_login "prod_sorts" "3600" \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && sops_export_vars 'sorts/secrets.yaml' \
      'FERNET_TOKEN' \
      'MIXPANEL_API_TOKEN_SORTS' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && groups_file="$(mktemp)" \
    && sorted_groups_file="$(mktemp)" \
    && list_groups "${groups_file}" \
    && sort "${groups_file}" -o "${sorted_groups_file}" \
    && execute_chunk_parallel execute "${sorted_groups_file}" "${parallel}" "batch"

}

main "${@}"
