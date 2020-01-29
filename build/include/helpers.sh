# shellcheck shell=bash

function _is_var_present {
  local var_name="${1}"
  test -n "${!var_name:-}"
}

function camel_case_to_title_case {
  # Turn 'something_like_this' to 'SomethingLikeThis'
  IFS=_ read -ra str <<<"${1}"
  printf '%s' "${str[@]^}"
}

function decrypt_and_source {
  local encryption_key="${1}"
  local encrypted_file="${2}"

  echo "Unencrypting and sourcing: ${encrypted_file}"
  # shellcheck disable=SC1090
  source <( \
    gpg \
      --batch \
      --passphrase-fd 0 \
      --decrypt "${encrypted_file}" \
    <<< "${encryption_key}")
  echo
}

function ensure_environment_variable {
  # Make sure that the provided environment var is set
  local env_var_name

  while test "$#" -gt 0
  do
    env_var_name="${1}"

    if ! _is_var_present "${env_var_name}"
    then
      echo "INFO: environment variable '${env_var_name}' is required"
      return 1
    fi

    shift
  done

  return 0
}

function with_development_secrets {
  export ENCRYPTION_KEY
  ensure_environment_variable 'ENCRYPTION_KEY'
  decrypt_and_source "${ENCRYPTION_KEY}" './secrets/development.sh.asc'
}

function with_production_secrets {
  export ENCRYPTION_KEY_PROD
  ensure_environment_variable 'ENCRYPTION_KEY_PROD'
  decrypt_and_source "${ENCRYPTION_KEY_PROD}" './secrets/production.sh.asc'
}
