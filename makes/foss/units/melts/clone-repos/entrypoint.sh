# shellcheck shell=bash

function main {
  local group="${1:-}"
  export CI='true'
  export CI_COMMIT_REF_NAME='master'
  export PROD_AWS_ACCESS_KEY_ID
  export PROD_AWS_SECRET_ACCESS_KEY

  shopt -s nullglob \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
      PROD_SERVICES_AWS_ACCESS_KEY_ID \
      PROD_SERVICES_AWS_SECRET_ACCESS_KEY \
    && PROD_AWS_ACCESS_KEY_ID="${PROD_SERVICES_AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${PROD_SERVICES_AWS_SECRET_ACCESS_KEY}" \
    && use_git_repo_services \
    && for root in "${@:2}"; do
      echo "[INFO] cloning ${root} from ${group}" \
        && { USER=nobody melts resources --clone-from-customer-git "${group}" --name "${root}" || true; }
    done
}

main "${@}"
