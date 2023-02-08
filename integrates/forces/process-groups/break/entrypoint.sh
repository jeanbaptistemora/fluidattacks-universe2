# shellcheck shell=bash

function forces_failed {
  local token="${1}"
  local repo_name="${2}"
  local kind="${3}"
  local strictness="${4}"
  local exit_code

  set +e

  forces \
    -vvv \
    --token "${token}" \
    --repo-name "${repo_name}" \
    --"${kind}" \
    --"${strictness}"

  exit_code="${?}"

  set -e

  if [ "${exit_code}" != "0" ]; then
    info "Forces failed as expected."
  else
    error "Forces did not fail."
  fi
}

function main {
  : \
    && aws_login "prod_forces" "3600" \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && sops_export_vars "integrates/forces/secrets-prod.yaml" \
      group_break \
    && group_name=$(jq -r '.name' <<< "${group_break}") \
    && repo_name=$(jq -r '.repo_name' <<< "${group_break}") \
    && strictness=$(jq -r '.strictness' <<< "${group_break}") \
    && kind=$(jq -r '.kind' <<< "${group_break}") \
    && token=$(get_forces_token "${group_name}") \
    && info "Running forces for ${group_name}" \
    && forces_failed \
      "${token}" \
      "${repo_name}" \
      "${kind}" \
      "${strictness}"
}

main
