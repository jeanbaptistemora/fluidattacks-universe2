# shellcheck shell=bash

function job_code_upload {
  local group="${1}"
  local db
  local creds
  export AWS_DEFAULT_REGION="us-east-1"

  db=$(mktemp) \
    && creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
      SERVICES_API_TOKEN \
    && prod_db "${db}" \
    && prod_user "${creds}" \
    && export_notifier_key \
    && echo "[INFO] Working on ${group}" \
    && use_git_repo_services \
    && echo "[INFO] Cloning ${group}" \
    && CI=true \
      CI_COMMIT_REF_NAME='trunk' \
      melts drills --pull-repos "${group}" \
    && echo "[INFO] Uploading ${group}" \
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
    && success-indicators compound-job \
      --job 'code_upload' \
      --child "${group}" \
    && shopt -u nullglob \
    && rm -rf "groups/${group}/fusion/"

}

job_code_upload "${@}"
