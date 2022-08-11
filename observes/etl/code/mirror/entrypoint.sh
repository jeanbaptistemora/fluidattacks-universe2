# shellcheck shell=bash

function job_code_mirror {
  local group="${1}"
  local working_dir
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_SESSION_TOKEN
  export AWS_DEFAULT_REGION="us-east-1"

  working_dir=$(mktemp -d) \
    && if test -z "${group}"; then
      abort '[INFO] Please set the first argument to the group name'
    fi \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && pushd "${working_dir}" \
    && echo "[INFO] Working on ${group}" \
    && echo "[INFO] Cloning ${group} from source Git repository" \
    && export CI='true' \
    && export CI_COMMIT_REF_NAME='trunk' \
    && export PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    && export PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    && { USER=nobody melts resources --clone-from-customer-git "${group}" || true; } \
    && if find "./groups/${group}/fusion/"* -maxdepth 0 -type d; then
      echo '[INFO] Pushing repositories to S3' \
        && USER=nobody melts drills --push-repos "${group}" \
        && chmod -R 777 groups \
        && rm -r groups
    else
      echo '[WARNING] Unable to clone repositories from source' \
        && echo '[WARNING] Connection failed or repo has not been updated' \
        && echo '[WARNING] Skipping push to S3'
    fi \
    && popd \
    || return 1
}

job_code_mirror "${@}"
