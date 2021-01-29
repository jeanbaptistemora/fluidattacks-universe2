# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'
source '__envUtilsBashLibGit__'

export PATH="__envUpdateSyncDateBin__:${PATH:-}"
melts='__envMelts__'

function job_code_mirror {
  local group="${1}"
  local TEMP_FILE
  TEMP_FILE=$(mktemp)

      if test -z "${group}"
      then
            echo '[INFO] Please set the first argument to the group name' \
        &&  return 1
      fi \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' 'default' \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE}" \
  &&  use_git_repo_services \
    &&  echo "[INFO] Working on ${group}" \
    &&  echo "[INFO] Cloning ${group} from source Git repository" \
    &&  export CI='true' \
    &&  export CI_COMMIT_REF_NAME='master' \
    &&  export PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    &&  export PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    &&  { "${melts}" resources --clone-from-customer-git "${group}" || true;} \
    &&  if find "groups/${group}/fusion/"* -maxdepth 0 -type d
        then
              echo '[INFO] Pushing repositories to S3' \
          &&  "${melts}" drills --push-repos "${group}" \
          &&  echo '[INFO] Updating last sync date' \
          &&  update-sync-date "${group}" "${TEMP_FILE}"
        else
              echo '[INFO] Unable to clone repositories from source' \
          &&  echo '[INFO] Skipping push to S3' \
          &&  return 1
        fi \
    &&  rm -rf "groups/${group}/fusion/" \
  &&  popd \
  ||  return 1
}

job_code_mirror "${@}"
