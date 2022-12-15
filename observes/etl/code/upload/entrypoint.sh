# shellcheck shell=bash

function job_code_upload {
  local group="${1}"
  local db
  local creds
  local migration_groups_file
  local migrated_groups_file
  export AWS_DEFAULT_REGION="us-east-1"

  db=$(mktemp) \
    && creds=$(mktemp) \
    && migration_groups_file=$(mktemp) \
    && migrated_groups_file=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
      SERVICES_API_TOKEN \
    && prod_db "${db}" \
    && prod_user "${creds}" \
    && export_notifier_key \
    && sops_export_vars 'observes/conf/code_migration.json' \
      migration \
      migrated \
    && echo "${migration}" | jq -rc '.[]' > "${migration_groups_file}" \
    && echo "${migrated}" | jq -rc '.[]' > "${migrated_groups_file}" \
    && readarray -t migration_groups < "${migration_groups_file}" \
    && readarray -t migrated_groups < "${migrated_groups_file}" \
    && if [[ ! ${migration_groups[*]} =~ ${group} ]]; then
      echo "[INFO] Working on ${group}" \
        && use_git_repo_services \
        && echo "[INFO] Cloning ${group}" \
        && if CI=true \
          CI_COMMIT_REF_NAME='trunk' \
          melts drills --pull-repos "${group}"; then
          echo "[INFO] Uploading ${group}" \
            && shopt -s nullglob \
            && observes-etl-code \
              --db-id "${db}" \
              --creds "${creds}" \
              upload-code \
              --arm-token "${INTEGRATES_API_TOKEN}" \
              --namespace "${group}" \
              --mailmap '.groups-mailmap' \
              "groups/${group}/fusion/"* \
            && echo "[INFO] Amend authors of ${group}" \
            && observes-etl-code \
              --db-id "${db}" \
              --creds "${creds}" \
              amend-authors \
              --namespace "${group}" \
              --mailmap '.groups-mailmap' \
            && if [[ ${migrated_groups[*]} =~ ${group} ]]; then
              echo "[INFO] Migrated group procedure" \
                && echo "[ERROR] Not defined" \
                && return 1
            fi \
            && shopt -u nullglob \
            && rm -rf "groups/${group}/fusion/"
        fi \
        && popd \
        || return 1
    else
      echo "[Skipped] ${group} migration in progress"
    fi

}

job_code_upload "${@}"
