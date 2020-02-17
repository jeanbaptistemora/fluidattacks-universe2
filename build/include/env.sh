# shellcheck shell=bash

source "${srcIncludeHelpers}"

function prepare_environment_variables {
  export IS_LOCAL_BUILD

      echo '[INFO] Sourcing .envrc.public' \
  &&  source './.envrc.public' \
  &&  if test -n "${GITLAB_CI:-}"
      then
            echo '[INFO] In remote build system' \
        && IS_LOCAL_BUILD="${FALSE}"
      else
            echo '[INFO] In local build system' \
        && IS_LOCAL_BUILD="${TRUE}"
      fi
}

function prepare_ephemeral_vars {
  export MYPY_CACHE_DIR
  export TEMP_FD
  export TEMP_FILE1
  export TEMP_FILE2

  MYPY_CACHE_DIR=$(mktemp)
  exec {TEMP_FD}>TEMP_FD
  TEMP_FILE1=$(mktemp)
  TEMP_FILE2=$(mktemp)
}

function prepare_python_packages {
  export PATH
  export PYTHONPATH="${PWD}"
  local pkg

  echo '[INFO] Preparing python packages'

  helper_list_vars_with_regex 'pyPkg[a-zA-Z0-9]+' > "${TEMP_FILE1}"

  while read -r pkg
  do
    echo "  [${pkg}] ${!pkg}"
    PATH="${PATH}:${!pkg}/site-packages/bin"
    PYTHONPATH="${PYTHONPATH}:${!pkg}/site-packages"
  done < "${TEMP_FILE1}"
}

function prepare_workdir {
  export WORKDIR="${PWD}.ephemeral"
  export STARTDIR="${PWD}"

      echo '[INFO] Creating a pristine workdir' \
  &&  rm -rf "${WORKDIR}" \
  &&  mkdir -p "${WORKDIR}" \
  &&  echo '[INFO] Copying files to workdir' \
  &&  cp -r "${STARTDIR}/." "${WORKDIR}" \
  &&  echo '[INFO] Entering the workdir' \
  &&  pushd "${WORKDIR}" \
  &&  trap 'teardown_workdir' 'EXIT' \
  ||  return 1
}

function teardown_workdir {
      echo "[INFO] Deleting: ${WORKDIR}" \
  &&  rm -rf "${WORKDIR}"
}
