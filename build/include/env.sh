# shellcheck shell=bash

source "${srcIncludeHelpers}"

function prepare_environment_variables {
  export IS_LOCAL_BUILD

      echo '[INFO] Sourcing .envrc.public' \
  &&  source './.envrc.public' \
  &&  if test -n "${GITLAB_CI:-}"
      then
            echo '[INFO] In local build system' \
        && IS_LOCAL_BUILD="${TRUE}"
      else
            echo '[INFO] In remote build system' \
        && IS_LOCAL_BUILD="${FALSE}"
      fi
}

function prepare_ephemeral_vars {
  export MYPY_CACHE_DIR
  export TEMP_FD
  export TEMP_FILE

  MYPY_CACHE_DIR=$(mktemp)
  exec {TEMP_FD}>TEMP_FD
  TEMP_FILE=$(mktemp)
}

function prepare_python_packages {
  export PATH
  export PYTHONPATH="${PWD}"
  local pkg

  echo '[INFO] Preparing python packages'

  helper_list_vars_with_regex 'pyPkg[a-zA-Z]+' > "${TEMP_FILE}"

  while read -r pkg
  do
    echo "  [${pkg}] ${!pkg}"
    PATH="${PATH}:${!pkg}/site-packages/bin"
    PYTHONPATH="${PYTHONPATH}:${!pkg}/site-packages"
  done < "${TEMP_FILE}"
}

function prepare_workdir {
  export WORKDIR
  export PRE_COMMIT_HOME

    WORKDIR=$(readlink -f "${PWD}/../serves.ephemeral") \
  && echo '[INFO] Creating a pristine workdir' \
  && rm -rf "${WORKDIR}" \
  && echo '[INFO] Adding a pristine workdir' \
  && cp -r . "${WORKDIR}"
}
