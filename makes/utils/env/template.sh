# shellcheck shell=bash

function export_product_variable {
  local var_name="${1}"
  local api_token
  local var_value

  if test -n "${GITLAB_API_TOKEN:-}"
  then
    api_token="${GITLAB_API_TOKEN}"
  elif test -n "${PRODUCT_API_TOKEN:-}"
  then
    api_token="${PRODUCT_API_TOKEN}"
  else
    abort '[CRITICAL] Missing GITLAB_API_TOKEN and PRODUCT_API_TOKEN'
  fi

  if var_value="$(get_project_variable "${api_token}" "${CI_PROJECT_ID}" "${var_name}")"
  then
    export "${var_name}"="${var_value}"
  else
    abort "[CRITICAL] ${var_name} is not present in the environment, also not on Gitlab"
  fi
}

function ensure_env_var {
  local var_name="${1}"

  if test -z "${!var_name:-}"
  then
    abort "[INFO] Variable is not present in the environment: ${var_name}"
  fi
}

function ensure_gitlab_env_var {
  local var_name="${1}"

  if test -z "${!var_name:-}"
  then
    export_product_variable "${var_name}"
  fi
}

function ensure_env_vars {
  for var_name in "${@}"
  do
        ensure_env_var "${var_name}" \
    ||  return 1
  done
}

function ensure_gitlab_env_vars {
  for var_name in "${@}"
  do
        ensure_gitlab_env_var "${var_name}" \
    ||  return 1
  done
}
