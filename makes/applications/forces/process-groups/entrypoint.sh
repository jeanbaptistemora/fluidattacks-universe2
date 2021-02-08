# shellcheck shell=bash

source '__envUtilsBashLibGit__'
source '__envUtilsSops__'


function main {

      sops_export_vars "forces/secrets-prod.yaml" \
        groups_to_check \
  &&  use_git_repo_services \
  &&  echo "${groups_to_check}" | '__envJq__/bin/jq' -c '.[]' -r | while read -r group; do
            echo "[INFO] Runing forces for ${group}" \
        &&  sops_export_vars "groups/${group}/config/secrets-dev.yaml" \
              forces_api_token \
        &&  '__envForces__' --token "${forces_api_token}" -vvv
      done \
  &&  popd || return 1
}

main
