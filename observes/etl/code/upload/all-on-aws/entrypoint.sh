# shellcheck shell=bash

function job_code_mirror_all_groups {
  local groups_file
  groups_file=$(mktemp)

  list_groups "${groups_file}" \
    && while read -r group; do
      echo "[INFO] Submitting: ${group}" \
        && __argCodeEtlUpload__ "${group}" \
        || return 1
    done < "${groups_file}"
}

job_code_mirror_all_groups
