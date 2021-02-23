# shellcheck shell=bash

source '__envUtilsSops__'
source '__envUtilsAws__'
source '__envUtilsMeltsLibCommon__'


function main {
      aws_login_prod forces \
  &&  sops_export_vars "forces/secrets-prod.yaml" \
        groups_to_check \
  &&   jq -c '.[]' -r <<< "${groups_to_check}" | while read -r group; do
            echo "[INFO] Runing forces for ${group}" \
        &&  forces --token "$(get_forces_token "${group}")" -vvv
      done \
  &&  popd || return 1
}

main
