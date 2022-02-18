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
  export PROD_SERVICES_AWS_ACCESS_KEY_ID
  export PROD_SERVICES_AWS_SECRET_ACCESS_KEY
  local group="${1}"

  echo '[INFO] Cloning repositories' \
    && CI='true' \
      CI_COMMIT_REF_NAME='master' \
      PROD_AWS_ACCESS_KEY_ID="${PROD_SERVICES_AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${PROD_SERVICES_AWS_SECRET_ACCESS_KEY}" \
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
    && if test -d "${cache_local}"; then
      case "${command}" in
        pull) aws_s3_sync "${cache_remote}" "${cache_local}" --delete ;;
        push) aws_s3_sync "${cache_local}" "${cache_remote}" --delete ;;
        *) abort "[CRITICAL] cache command must be one of: pull, push" ;;
      esac
    else
      echo "[WARNING] the cache directory ${cache_local} does not exist"
    fi
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

function execute_skims_combination {
  local group="${1}"
  local namespace="${2}"
  local config
  export checks=()

  if test -e "groups/${group}/fusion/${namespace}"; then
    for check in $(echo "${CHECKS}" | jq -r '.[] | @base64'); do
      check="$(echo "${check}" | base64 --decode)" \
        && if skims_should_run "${group}" "${namespace}" "${check}"; then
          checks=("${checks[@]}" "${check}")
        fi
    done \
      && if test "${#checks[@]}" -gt 0; then
        skims_rebase "${group}" "${namespace}" \
          && config="$(mktemp)" \
          && echo "[INFO] Running skims scan in ${group}" \
          && lang="$(get_skims_language "${group}")" \
          && python3 __argGetConfig__ --check "${checks[@]}" \
            --group "${group}" \
            --language "${lang}" \
            --namespace "${namespace}" \
            --out "${config}" \
          && skims scan --group "${group}" "${config}"
      else
        echo "[WARNING] there are no findings to run"
      fi
  else
    echo "[ERROR] repos no not cloned: ${namespace}"
  fi
}

function get_all_roots {
  group="${1}"
  curl 'https://app.fluidattacks.com/api' \
    -H "authorization: Bearer ${INTEGRATES_API_TOKEN}" \
    -H 'content-type: application/json' \
    -d "{\"operationName\":\"GetRoots\",\"variables\":{\"groupName\":\"${group}\"},\"query\":\"query GetRoots(\$groupName: String\\u0021) { group(groupName: \$groupName) { roots { ... on GitRoot { nickname state}}}}\"}" \
    --silent \
    --compressed | jq '.data.group.roots | map(select(.state == "ACTIVE")) | map(.nickname)'
}

function main {
  export CHECKS

  local group="${1:-}"
  local roots="${3:-}" # must be in json forma
  local config

  export -f execute_skims_combination
  export -f skims_rebase
  export -f get_skims_language
  export -f get_skims_expected_code_date
  export -f skims_cache
  export -f skims_should_run
  export -f from_epoch_to_iso8601
  export -f from_iso8601_to_epoch
  export -f aws_s3_sync

  check_cli_arg 1 group "${group}" \
    && shopt -s nullglob \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
      PROD_SERVICES_AWS_ACCESS_KEY_ID \
      PROD_SERVICES_AWS_SECRET_ACCESS_KEY \
    && if [ -z "${roots}" ] && [ -n "${MACHINE_ALL_ROOTS}" ]; then
      roots="$(get_all_roots "${group}")" # must be in json forma
    fi \
    && if [ -n "${2}" ]; then
      CHECKS="${2}" # must be in json forma
    fi \
    && config="$(mktemp)" \
    && roots="$(jq -r -c '.[]' <<< "${roots}")" \
    && use_git_repo_services \
    && clone_group "${group}" \
    && aws_login_prod 'skims' \
    && parallel "${parallel_args[@]}" execute_skims_combination "${group}" ::: "${roots}" \
    && skims_cache push "${group}" \
    && popd \
    && clean_file_system "${group}"
}

main "${@}"
