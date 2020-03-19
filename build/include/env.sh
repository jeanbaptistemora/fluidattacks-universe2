# shellcheck shell=bash

source "${srcIncludeHelpers}"

function env_prepare_environment_variables {
  export IS_LOCAL_BUILD
  export ENVIRONMENT_NAME
  export STARTDIR="${PWD}"
  export WORKDIR="${PWD}.ephemeral"

      echo '[INFO] Sourcing .envrc.public' \
  &&  source './.envrc.public' \
  &&  if test -n "${CI:-}"
      then
            echo '[INFO] In remote build system' \
        && IS_LOCAL_BUILD="${FALSE}"
      else
            echo '[INFO] In local build system' \
        && IS_LOCAL_BUILD="${TRUE}"
      fi \
  &&  if test "${CI_COMMIT_REF_NAME}" = 'master'
      then
            echo '[INFO] In productive environment' \
        &&  ENVIRONMENT_NAME='prod'
      else
            echo '[INFO] In development environment' \
        &&  ENVIRONMENT_NAME='dev'
      fi
}

function env_prepare_ephemeral_vars {
  export MYPY_CACHE_DIR
  export TEMP_FD
  export TEMP_FILE1
  export TEMP_FILE2

  MYPY_CACHE_DIR=$(mktemp)
  exec {TEMP_FD}>TEMP_FD
  TEMP_FILE1=$(mktemp)
  TEMP_FILE2=$(mktemp)
}

function env_prepare_python_packages {
  export PATH
  export PYTHONPATH
  local pkg

  echo '[INFO] Preparing ephemeral variables'

  env_prepare_ephemeral_vars

  echo '[INFO] Preparing python packages'

  helper_list_vars_with_regex 'pyPkg[a-zA-Z0-9]+' > "${TEMP_FILE1}"

  while read -r pkg
  do
    echo "  [${pkg}] ${!pkg}"
    PATH="${PATH}:${!pkg}/site-packages/bin"
    PYTHONPATH="${!pkg}/site-packages:${PYTHONPATH:-}"
  done < "${TEMP_FILE1}"
}
