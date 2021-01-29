# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'
source '__envUtilsBashLibGit__'
export PATH="__envMirrorGroupBin__:${PATH:-}"

function list_services_groups {
  local store="${1}"
      use_git_repo_services \
    &&  ls -1 groups/ > "${store}" \
  &&  popd \
  ||  return 1
}

function job_code_mirror_all_groups {
  local groups_file
  groups_file=$(mktemp)

      list_services_groups "${groups_file}" \
  &&  while read -r group
      do
            echo "[INFO] Submitting: ${group}" \
        &&  aws-batch-code-etl-mirror "${group}" \
        ||  return 1
      done < "${groups_file}"
}

job_code_mirror_all_groups
