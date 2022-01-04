# shellcheck shell=bash

alias code-etl="observes-etl-code-bin"

function job_code_upload {
  local group="${1}"
  local db
  local creds

  db=$(mktemp) \
    && creds=$(mktemp) \
    && aws_login_prod_new 'observes' \
    && prod_db "${db}" \
    && prod_user "${creds}" \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && use_git_repo_services \
    && echo "[INFO] Working on ${group}" \
    && echo "[INFO] Cloning ${group}" \
    && if CI=true \
      CI_COMMIT_REF_NAME='master' \
      PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
      melts drills --pull-repos "${group}"; then
      echo "[INFO] Uploading ${group}" \
        && shopt -s nullglob \
        && code-etl upload-code \
          "${group}" \
          "groups/${group}/fusion/"* \
          --mailmap '.groups-mailmap' \
        && code-etl v2 \
          --db-id "${db}" \
          --creds "${creds}" \
          amend-authors-v2 \
          --schema 'code' \
          --table 'commits' \
          --namespace "${group}" \
          --mailmap '.groups-mailmap' \
        && shopt -u nullglob \
        && rm -rf "groups/${group}/fusion/"

    fi \
    && popd \
    || return 1

}

job_code_upload "${@}"
