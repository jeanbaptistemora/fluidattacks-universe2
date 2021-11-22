# shellcheck shell=bash

function check_cli_arg {
  local pos="${1}"
  local name="${2}"
  local value="${3}"

  if test -z "${value}"; then
    abort "[ERROR] Please specify ${name} as positional argument #${pos}"
  fi
}

function clean_file_system {
  local group="${1}"
  local paths=(
    ~/.skims
    "groups/${group}/fusion"
  )

  rm -rf "${paths[@]}" || true
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

function clone_group {
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  local group="${1}"

  echo '[INFO] Cloning repositories' \
    && CI='true' \
      CI_COMMIT_REF_NAME='master' \
      PROD_AWS_ACCESS_KEY_ID="${SERVICES_PROD_AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${SERVICES_PROD_AWS_SECRET_ACCESS_KEY}" \
      melts drills --pull-repos "${group}" \
    && for namespace in "groups/${group}/fusion/"*; do
      echo "        - ${namespace}"
    done
}

function skims_cache {
  local command="${1}"
  local group="${2}"
  local cache_local=~/.skims/cache
  local cache_remote="s3://skims.data/cache/${group}/"

  echo "[INFO] Cache ${command}" \
    && case "${command}" in
      pull) aws_s3_sync "${cache_remote}" "${cache_local}" --delete ;;
      push) aws_s3_sync "${cache_local}" "${cache_remote}" --delete ;;
      *) abort "[CRITICAL] cache command must be one of: pull, push" ;;
    esac
}

function skims_rebase {
  local group="${1}"
  local namespace="${2}"

  skims rebase \
    --group "${group}" \
    --namespace "${namespace}" \
    "groups/${group}/fusion/${namespace}" \
    || true
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
    && expected_code_date_epoch="$(get_skims_expected_code_date "${group}" "${namespace}" "${check}")" \
    && expected_code_date="$(from_epoch_to_iso8601 "${expected_code_date_epoch}")" \
    && if test -e "${metadata}" && metadata_date=$(jq -er '.date' < "${metadata}"); then
      echo "[INFO] Git data for ${group} ${namespace} is at ${metadata_date}" \
        && metadata_date_epoch="$(from_iso8601_to_epoch "${metadata_date}")" \
        && echo "[INFO] Skims expected code date for ${group} ${namespace} is ${expected_code_date}" \
        && test "${metadata_date_epoch}" -ge "${expected_code_date_epoch}"
    else
      echo "[INFO] Either ${metadata} does not exist or it is corrupt" \
        && return 1
    fi
}

function skims_scan {
  local group="${1}"
  local namespace="${2}"
  local check="${3}"
  local config="${4}"

  echo "[INFO] Running skims scan" \
    && lang="$(get_skims_language "${group}")" \
    && python3 __argGetConfig__ --check "${check}" \
      --group "${group}" \
      --language "${lang}" \
      --namespace "${namespace}" \
      --out "${config}" \
    && skims scan --group "${group}" "${config}"
}

function execute_skims_combination {
  local group="${1}"
  local namespace="${2}"
  local check="${3}"
  local config

  if test -e "groups/${group}/fusion/"; then
    skims_rebase "${group}" "${namespace}" \
      && config="$(mktemp)" \
      && skims_should_run "${group}" "${namespace}" "${check}" \
      && if skims_scan "${group}" "${namespace}" "${check}" "${config}"; then
        echo "[INFO] Succesfully processed: ${group} ${namespace}"
      else
        echo "[ERROR] While running skims on: ${group} ${namespace}"
      fi \
      && skims_cache push "${group}" "${check}" "${namespace}"
  else
    echo "[ERROR] repos no not cloned: ${namespace}"
  fi
}

function main {
  local group="${1:-}"
  local checks="${2:-}" # must be in json forma
  local config

  export -f execute_skims_combination
  export -f skims_rebase
  export -f get_skims_language
  export -f get_skims_expected_code_date
  export -f skims_cache
  export -f skims_scan
  export -f skims_should_run
  export -f from_epoch_to_iso8601
  export -f from_iso8601_to_epoch
  export -f aws_s3_sync

  check_cli_arg 1 group "${group}" \
    && shopt -s nullglob \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
      SERVICES_PROD_AWS_ACCESS_KEY_ID \
      SERVICES_PROD_AWS_SECRET_ACCESS_KEY \
    && config="$(mktemp)" \
    && checks="$(jq -r -c '.[]' <<< "${checks}")" \
    && use_git_repo_services \
    && clone_group "${group}" \
    && aws_login_prod 'skims' \
    && skims_cache pull "${group}" \
    && parallel execute_skims_combination "${group}" ::: "$(ls "groups/${group}/fusion/")" ::: "${checks}" \
    && skims_cache push "${group}" \
    && popd \
    && clean_file_system "${group}"
}

main "${@}"
