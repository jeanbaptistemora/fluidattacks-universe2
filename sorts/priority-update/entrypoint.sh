# shellcheck shell=bash

function update_priority {
  local group="${1}"
  local success

  mkdir -p groups/"${group}" \
    && echo '[INFO] Running sorts priority update:' \
    && if sorts --update-group-priority "groups/${group}" "${current_date}"; then
      echo "[INFO] Succesfully executed on: ${group}" \
        && success='true'
    else
      echo "[ERROR] While running Sorts on: ${group}" \
        && success='false'
    fi \
    && rm -rf "groups/${group}" \
    && test "${success}" = 'true'
}

function main {
  local parallel="${1}"
  local groups_file
  current_date="$(date +"%Y-%m-%d")"

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
    && list_groups "${groups_file}" \
    && execute_chunk_parallel update_priority "${groups_file}" "${parallel}" "batch"

}

main "${@}"
