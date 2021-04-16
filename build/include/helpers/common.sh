# shellcheck shell=bash

function helper_common_use_pristine_workdir {
  export WORKDIR
  export STARTDIR

  function helper_teardown_workdir {
        echo "[INFO] Deleting: ${WORKDIR}" \
    &&  pushd "${STARTDIR}" \
    &&  git worktree remove -f "${WORKDIR}" \
    &&  rm -rf "${WORKDIR}"
  }

      echo '[INFO] Creating a pristine workdir' \
  &&  rm -rf "${WORKDIR}" \
  &&  git worktree add -f "${WORKDIR}" "${CI_COMMIT_REF_NAME}" \
  &&  pushd "${WORKDIR}" \
  &&  trap 'helper_teardown_workdir' 'EXIT' \
  ||  return 1
}

function helper_common_list_declared_jobs {
  local product="${1:-}"

  declare -F \
    | sed 's/declare -f //' \
    | grep -P '^job_[a-z_]+' \
    | sed 's/job_//' \
    | grep -P "${product}" \
    | sort
}

function helper_common_list_vars_with_regex {
  local regex="${1}"
  printenv | grep -oP "${regex}" | sort
}
