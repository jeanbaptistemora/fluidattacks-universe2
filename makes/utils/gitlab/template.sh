# shellcheck shell=bash

function __check_curl_output {
  local success_msg="${1}"
  local failure_msg="${2}"
  local curl_status_code="${3}"
  local expected_status_code="${4}"
  local log_file="${5}"

  if [[ ${curl_status_code} =~ ${expected_status_code} ]]; then
    echo "${success_msg}" \
      && return 0
  else
    echo "${failure_msg}" \
      && echo "[ERROR] Expected HTTP ${expected_status_code} but got HTTP ${curl_status_code}" \
      && echo '[INFO] Displaying curl output' \
      && cat "${log_file}" \
      && echo \
      && return 1
  fi
}

function __project_variable_generic_request {
  local http_verb="${1}"
  local url="${2}"
  local success_msg="${3}"
  local failure_msg="${4}"
  local token="${5}"
  local repo_id="${6}"
  local var_name="${7}"
  local var_value="${8}"
  local protected="${9}"
  local masked="${10}"
  local curl_status_code
  local log_file

  log_file=$(mktemp) \
    && echo '[INFO] Performing curl command' \
    && curl_status_code=$(
      curl --form "key=${var_name}" \
        --form "value=${var_value}" \
        --form "protected=${protected}" \
        --form "masked=${masked}" \
        --header "private-token: ${token}" \
        --location \
        --output "${log_file}" \
        --request "${http_verb}" \
        --silent \
        --write-out "%{http_code}" \
        "${url}" \
        || true
    ) \
    && __check_curl_output \
      "${success_msg}" \
      "${failure_msg}" \
      "${curl_status_code}" '2..' \
      "${log_file}"
}

function set_project_variable {
  local token="${1}"
  local repo_id="${2}"
  local var_name="${3}"
  local var_value="${4}"
  local protected="${5}"
  local masked="${6}"

  echo "[INFO] Setting gitlab variable ${var_name} in project ${repo_id}:" \
    && if check_variable_exists "${token}" "${repo_id}" "${var_name}"; then
      update_project_variable \
        "${token}" \
        "${repo_id}" \
        "${var_name}" \
        "${var_value}" \
        "${protected}" \
        "${masked}"
    else
      create_project_variable \
        "${token}" \
        "${repo_id}" \
        "${var_name}" \
        "${var_value}" \
        "${protected}" \
        "${masked}"
    fi
}

function check_variable_exists {
  local token="${1}"
  local repo_id="${2}"
  local var_name="${3}"
  local curl_status_code
  local log_file

  log_file=$(mktemp) \
    && echo '[INFO] Performing curl command' \
    && curl_status_code=$(
      curl --header "private-token: ${token}" \
        --location \
        --output "${log_file}" \
        --silent \
        --write-out "%{http_code}" \
        "https://gitlab.com/api/v4/projects/${repo_id}/variables/${var_name}" \
        || true
    ) \
    && __check_curl_output \
      "[INFO] Variable exists: ${var_name}" \
      "[INFO] Variable does not exist: ${var_name}" \
      "${curl_status_code}" '200' \
      "${log_file}"
}

function create_project_variable {
  local token="${1}"
  local repo_id="${2}"
  local var_name="${3}"
  local var_value="${4}"
  local protected="${5}"
  local masked="${6}"
  local curl_status_code
  local log_file

  __project_variable_generic_request \
    'POST' \
    "https://gitlab.com/api/v4/projects/${repo_id}/variables" \
    "[INFO] Variable created successfully: ${var_name}" \
    "[ERROR] Variable was not created: ${var_name}" \
    "${token}" \
    "${repo_id}" \
    "${var_name}" \
    "${var_value}" \
    "${protected}" \
    "${masked}"
}

function get_project_variable {
  local token="${1}"
  local repo_id="${2}"
  local var_name="${3}"

  api_url="https://gitlab.com/api/v4/projects/${repo_id}/variables" \
    && echo "[INFO] Retrieving var from GitLab: ${var_name}" 1>&2 \
    && curl \
      --silent \
      --header "private-token: ${token}" \
      "${api_url}/${var_name}" \
    | jq -er '.value'
}

function update_project_variable {
  local token="${1}"
  local repo_id="${2}"
  local var_name="${3}"
  local var_value="${4}"
  local protected="${5}"
  local masked="${6}"
  local curl_status_code
  local log_file

  __project_variable_generic_request \
    'PUT' \
    "https://gitlab.com/api/v4/projects/${repo_id}/variables/${var_name}" \
    "[INFO] Variable updated successfully: ${var_name}" \
    "[ERROR] Variable was not updated: ${var_name}" \
    "${token}" \
    "${repo_id}" \
    "${var_name}" \
    "${var_value}" \
    "${protected}" \
    "${masked}"
}

### Tests

function _tests {
  local token="${1}"

  set -u

  check_variable_exists "${token}" '4603023' 'INTEGRATES_API_TOKEN' \
    && echo '[TEST][should-success] Ok' \
    || echo '[TEST][should-success] Review!!'
  echo ---
  check_variable_exists "${token}" '4603023' 'INTEGRATES_API_TOKE' \
    && echo '[TEST][should-fail] Review!!' \
    || echo '[TEST][should-fail] Ok'
  echo ---
  set_project_variable "${token}" '4603023' 'test_var' 'test_value' 'true' 'true' \
    && echo '[TEST][should-success] Ok' \
    || echo '[TEST][should-success] Review!!'
  echo ---
  # Something that cannot be masked
  set_project_variable "${token}" '4603023' 'test_var' '^^^^' 'true' 'true' \
    && echo '[TEST][should-fail] Review!!' \
    || echo '[TEST][should-fail] Ok'
  echo ---
  # Random var name and value but can be masked
  set_project_variable "${token}" '4603023' "$(mktemp test_XXX)" "$(mktemp test_XXX)" 'true' 'true' \
    && echo '[TEST][should-success] Ok' \
    || echo '[TEST][should-success] Review!!'
}
