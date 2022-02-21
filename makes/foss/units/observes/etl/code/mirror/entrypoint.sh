# shellcheck shell=bash

function job_code_mirror {
  local group="${1}"
  local db_creds

  true \
    && if test -z "${group}"; then
      abort '[INFO] Please set the first argument to the group name'
    fi \
    && db_creds=$(mktemp) \
    && aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_redshift}" > "${db_creds}" \
    && use_git_repo_services \
    && echo "[INFO] Working on ${group}" \
    && echo "[INFO] Cloning ${group} from source Git repository" \
    && export CI='true' \
    && export CI_COMMIT_REF_NAME='master' \
    && export PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    && export PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    && { USER=nobody melts resources --clone-from-customer-git "${group}" || true; } \
    && if find "groups/${group}/fusion/"* -maxdepth 0 -type d; then
      echo '[INFO] Pushing repositories to S3' \
        && USER=nobody melts drills --push-repos "${group}" \
        && rm -rf "groups/${group}/fusion/"
    else
      echo '[WARNING] Unable to clone repositories from source' \
        && echo '[WARNING] Connection failed or repo has not been updated' \
        && echo '[WARNING] Skipping push to S3'
    fi \
    && popd \
    || return 1
}

job_code_mirror "${@}"
