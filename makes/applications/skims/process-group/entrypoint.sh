# shellcheck shell=bash

function check_cli_arg {
  local pos="${1}"
  local name="${2}"
  local value="${3}"

  if test -z "${value}"
  then
    abort "[ERROR] Please specify ${name} as positional argument #${pos}"
  fi
}

function get_skims_language {
  local group="${1}"

  skims language --group "${group}"
}

function get_skims_expected_code_date {
  local group="${1}"
  local namespace="${2}"
  local check="${3}"

  skims expected-code-date \
    --finding-code "${check}" \
    --group "${group}" \
    --namespace "${namespace}"
}

function update_group {
  local group="${1}"

      echo '[INFO] Updating repositories mirror on S3' \
  &&  observes-scheduled-job-code-etl-mirror "${group}"
}

function clone_group {
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  local group="${1}"

      echo '[INFO] Cloning repositories' \
  &&  CI='true' \
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

function skims_rebase {
  local group="${1}"
  local namespace="${2}"

      skims rebase \
        --group "${group}" \
        --namespace "${namespace}" \
        "groups/${group}/fusion/${namespace}" \
  ||  true
}

function skims_should_run {
  local group="${1}"
  local namespace="${2}"
  local check="${3}"
  local metadata="groups/${group}/fusion/${namespace}/.git/fluidattacks_metadata"

  local expected_code_date
  local expected_code_date_epoch
  local metadata_date
  local metadata_date_epoch

      echo "[INFO] Checking if skims should run in ${group} ${namespace} ${check}" \
  &&  expected_code_date_epoch="$(get_skims_expected_code_date "${group}" "${namespace}" "${check}")" \
  &&  expected_code_date="$(from_epoch_to_iso8601 "${expected_code_date_epoch}")" \
  &&  if test -e "${metadata}" && metadata_date=$(jq -er '.date' < "${metadata}")
      then
            echo "[INFO] Git data for ${group} ${namespace} is at ${metadata_date}" \
        &&  metadata_date_epoch="$(from_iso8601_to_epoch "${metadata_date}")" \
        &&  echo "[INFO] Skims expected code date for ${group} ${namespace} is ${expected_code_date}" \
        &&  test "${metadata_date_epoch}" -ge "${expected_code_date_epoch}"
      else
            echo "[INFO] Either ${metadata} does not exist or it is corrupt" \
        &&  return 1
      fi
}

function skims_scan {
  local group="${1}"
  local namespace="${2}"
  local check="${3}"
  local lang="${4}"
  local config="${5}"

  local cache_local="${HOME_IMPURE}/.skims/cache"
  local cache_remote="s3://skims.data/cache/${group}/${namespace}"

      echo '[INFO] Running skims scan' \
  &&  python3 __envGetConfig__\
        --check "${check}" \
        --group "${group}" \
        --language "${lang}" \
        --namespace "${namespace}" \
        --out "${config}" \
  &&  echo '[INFO] Fetching cache' \
  &&  aws_s3_sync "${cache_remote}" "${cache_local}" \
  &&  if skims scan --group "${group}" "${config}"
      then
        echo "[INFO] Succesfully processed: ${group} ${namespace}"
      else
            echo "[ERROR] While running skims on: ${group} ${namespace}" \
        &&  success='false'
      fi \
  &&  echo '[INFO] Populating cache' \
  &&  aws_s3_sync "${cache_local}" "${cache_remote}"
}

function main {
  local group="${1:-}"
  local check="${2:-}"
  local config
  local success='true'

      check_cli_arg 1 group "${group}" \
  &&  check_cli_arg 2 check "${check}" \
  &&  shopt -s nullglob \
  &&  ensure_gitlab_env_vars \
        INTEGRATES_API_TOKEN \
        SERVICES_PROD_AWS_ACCESS_KEY_ID \
        SERVICES_PROD_AWS_SECRET_ACCESS_KEY \
  &&  config="$(mktemp)" \
  &&  lang="$(get_skims_language "${group}")" \
  &&  update_group "${group}" \
  &&  use_git_repo_services \
    &&  clone_group "${group}" \
    &&  aws_login_prod 'skims' \
    &&  for repo_path in "groups/${group}/fusion/"*
        do
              namespace="$(basename "${repo_path}")" \
          &&  skims_rebase "${group}" "${namespace}" \
          &&  skims_should_run "${group}" "${namespace}" "${check}" \
          &&  skims_scan "${group}" "${namespace}" "${check}" "${lang}" "${config}" \
          ||  continue
        done \
  &&  popd \
  &&  test "${success}" = 'true' \
  &&  report_success "${group}" "${check}"
}

main "${@}"
