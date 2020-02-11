# shellcheck shell=bash

source "${srcIncludeHelpers}"

function prepare_environment_variables {
    echo "[INFO] Sourcing .envrc.public" \
  && source './.envrc.public'
}

function prepare_ephemeral_vars {
  export TEMP_FD
  export TEMP_FILE

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
