# shellcheck shell=bash

function main {
  : \
    && aws_login "prod_forces" "3600" \
    && sops_export_vars "integrates/forces/secrets-prod.yaml" \
      groups_to_check \
    && jq -c '.[]' -r <<< "${groups_to_check}" | while read -r group; do
      group_name=$(jq -r '.name' <<< "${group}") \
      && repo_name=$(jq -r '.repo_name' <<< "${group}") \
        && strictness=$(jq -r '.strictness' <<< "${group}") \
        && kind=$(jq -r '.kind' <<< "${group}") \
        && echo "[INFO] Runing forces for ${group_name}" \
        && (forces \
          --token "$(get_forces_token "${group_name}")" \
          -vvv \
          --repo-name "${repo_name}" \
          --"${kind}" \
          --"${strictness}" || true)
    done
}

main
