# shellcheck shell=bash

function list_services_groups {
  local store="${1}"

  use_git_repo_services \
    && ls -1 groups/ > "${store}" \
    && popd \
    || return 1
}

function migration {
  local groups_file
  local init_index="${1}"
  local chunk="${2}"
  local groups

  groups_file=$(mktemp) \
    && list_services_groups "${groups_file}" \
    && readarray -t groups < "${groups_file}" \
    && for index in "${!groups[@]}"; do
      if test "${index}" -ge "${init_index}" && test "${index}" -lt $((init_index + chunk)); then
        echo "[INFO] Submitting: ${groups[index]}" \
          && __argMigrate__ "${groups[index]}" \
          || return 1
      fi
    done
}

migration "${@}"
