# shellcheck shell=bash

alias code-etl="observes-etl-code-bin"

function job_code_upload {
  local group="${1}"
  local db
  local creds
  local migration_groups_file
  local migrated_groups_file

  db=$(mktemp) \
    && creds=$(mktemp) \
    && migration_groups_file=$(mktemp) \
    && migrated_groups_file=$(mktemp) \
    && aws_login_prod_new 'observes' \
    && prod_db "${db}" \
    && prod_user "${creds}" \
    && sops_export_vars 'observes/conf/code_migration.json' \
      migration \
      migrated \
    && echo "${migration}" | jq -erc '.[]' > "${migration_groups_file}" \
    && echo "${migrated}" | jq -erc '.[]' > "${migrated_groups_file}" \
    && readarray -t migration_groups < "${migration_groups_file}" \
    && readarray -t migrated_groups < "${migrated_groups_file}" \
    && if [[ ! ${migration_groups[*]} =~ ${group} ]]; then
      echo "[INFO] Working on ${group}" \
        && use_git_repo_services \
        && echo "[INFO] Cloning ${group}" \
        && if CI=true \
          CI_COMMIT_REF_NAME='master' \
          PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
          PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
          melts drills --pull-repos "${group}"; then
          echo "[INFO] Uploading ${group}" \
            && shopt -s nullglob \
            && code-etl \
              --db-id "${db}" \
              --creds "${creds}" \
              upload-code \
              --schema 'code' \
              --table 'commits' \
              --namespace "${group}" \
              --mailmap '.groups-mailmap' \
              "groups/${group}/fusion/"* \
            && echo "[INFO] Amend authors of ${group}" \
            && code-etl \
              --db-id "${db}" \
              --creds "${creds}" \
              amend-authors \
              --schema 'code' \
              --table 'commits' \
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
