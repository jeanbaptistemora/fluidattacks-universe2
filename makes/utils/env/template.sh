# shellcheck shell=bash

function export_product_variable {
  local var_name="${1}"
  local var_value

  if test -n "${GITLAB_API_TOKEN:-}"
  then
    if var_value="$(get_project_variable "${GITLAB_API_TOKEN}" "${CI_PROJECT_ID}" "${var_name}")"
    then
      export "${var_name}"="${var_value}"
    else
      abort "[CRITICAL] ${var_name} is not present in the environment, also not on Gitlab"
    fi
  else
    abort '[CRITICAL] Unable to get variable from Gitlab, missing GITLAB_API_TOKEN'
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
