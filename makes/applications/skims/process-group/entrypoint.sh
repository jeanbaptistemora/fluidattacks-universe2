# shellcheck shell=bash

function clone_group {
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  local group="${1}"

      CI='true' \
      CI_COMMIT_REF_NAME='master' \
      PROD_AWS_ACCESS_KEY_ID="${SERVICES_PROD_AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${SERVICES_PROD_AWS_SECRET_ACCESS_KEY}" \
      melts drills --pull-repos "${group}" \
  &&  echo "[INFO] Repositories cloned:" \
  &&  for namespace in "groups/${group}/fusion/"*
      do
        echo "        - ${namespace}"
      done
}

function report_success {
  local group="${1}"
  local check="${2}"

      db_creds=$(mktemp) \
  &&  aws_login_prod 'observes' \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
  &&  echo "${analytics_auth_redshift}" > "${db_creds}" \
  &&  observes-bin-service-job-last-success single-job \
        --auth "${db_creds}" \
        --job "skims-process-group-${group}-${check}"
}

function main {
  local group="${1:-}"
  local check="${2:-}"
  local cache_local="${HOME_IMPURE}/.skims/cache"
  local cache_remote="s3://skims.data/cache/${group}"
  local config_file
  local success='true'

      if test -z "${group}"
      then
        abort '[ERROR] Specify the group on the first argument to this program'
      fi \
  &&  if test -z "${check}"
      then
        abort '[ERROR] Specify the check on the second argument to this program'
      fi \
  &&  echo "[INFO] Processing ${group}" \
  &&  shopt -s nullglob \
  &&  aws_login_prod 'skims' \
  &&  config_file=$(mktemp) \
  &&  language="$(melts misc --get-group-language "${group}")" \
  &&  use_git_repo_services \
    &&  echo '[INFO] Cloning repositories' \
    &&  clone_group "${group}" \
    &&  for namespace in "groups/${group}/fusion/"*
        do
              namespace="$(basename "${namespace}")" \
          &&  echo '[INFO] Running skims' \
          &&  python3 __envGetConfig__\
                --check "${check}" \
                --group "${group}" \
                --language "${language}" \
                --namespace "${namespace}" \
                --out "${config_file}" \
          &&  echo '[INFO] Fetching cache' \
          &&  aws_s3_sync "${cache_remote}/${namespace}" "${cache_local}" \
          &&  if skims --group "${group}" "${config_file}"
              then
                echo "[INFO] Succesfully processed: ${group} ${namespace}"
              else
                    echo "[ERROR] While running skims on: ${group} ${namespace}" \
                &&  success='false'
              fi \
          &&  echo '[INFO] Populating cache' \
          &&  aws_s3_sync "${cache_local}" "${cache_remote}/${namespace}" \
          ||  continue
        done \
  &&  popd \
  &&  test "${success}" = 'true' \
  &&  report_success "${group}" "${check}"
}

main "${@}"
