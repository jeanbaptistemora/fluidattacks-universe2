# shellcheck shell=bash

alias code-etl="observes-bin-code-etl"

function job_code_upload {
  local group="${1}"

  true \
    && if test -z "${group}"; then
      abort '[INFO] Please set the first argument to the group name'
    fi \
    && aws_login_prod 'observes' \
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
      echo "[INFO] Apending mailmaps" \
        && shopt -s nullglob \
        && for repo in "groups/${group}/fusion/"*; do
          cp -f '.groups-mailmap' "${repo}/.mailmap" \
            || return 1
        done \
        && echo "[INFO] Executing ${group}" \
        && code-etl upload-code \
          "${group}" \
          "groups/${group}/fusion/"* \
        && shopt -u nullglob \
        && rm -rf "groups/${group}/fusion/"

    fi \
    && popd \
    || return 1

}

job_code_upload "${@}"
