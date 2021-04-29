# shellcheck shell=bash

function execute {
  export INTEGRATES_API_TOKEN
  local group="${1}"
  local success

      { clone_services_repository "${group}" || true; } \
  &&  if ! test -e "groups/${group}/fusion"
      then
            echo '[WARNING] No repositories to test' \
        &&  return 0
      fi \
  &&  echo '[INFO] Running sorts:' \
  &&  if sorts "groups/${group}"
      then
            echo "[INFO] Succesfully executed on: ${group}" \
        &&  success='true'
      else
            echo "[ERROR] While running Sorts on: ${group}" \
        &&  success='false'
      fi \
  &&  upload_sorts_results_to_s3 "${group}" \
  &&  rm -rf "groups/${group}/fusion" \
  &&  test "${success}" = 'true'
}

function main {
  local groups_file

      use_git_repo_services \
  &&  groups_file="$(mktemp)" \
  &&  ls -1 groups > "${groups_file}" \
  &&  execute_chunk_parallel execute "${groups_file}"

}

main "${@}"
