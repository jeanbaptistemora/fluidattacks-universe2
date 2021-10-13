# shellcheck shell=bash

function list_services_groups {
  local store="${1}"

  use_git_repo_services \
    && ls -1 groups/ > "${store}" \
    && popd \
    || return 1
}

function job_code_mirror_all_groups {
  local groups_file
  groups_file=$(mktemp)

  list_services_groups "${groups_file}" \
    && while read -r group; do
      echo "[INFO] Submitting: ${group}" \
        && __argCodeEtlUpload__ "${group}" \
        || return 1
    done < "${groups_file}"
}

job_code_mirror_all_groups
