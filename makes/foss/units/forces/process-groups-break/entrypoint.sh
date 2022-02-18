# shellcheck shell=bash

function main {
  aws_login_prod forces \
    && sops_export_vars "forces/secrets-prod.yaml" \
      group_break \
    && group_name=$(jq -r '.name' <<< "${group_break}") \
    && repo_name=$(jq -r '.repo_name' <<< "${group_break}") \
    && strictness=$(jq -r '.strictness' <<< "${group_break}") \
    && kind=$(jq -r '.kind' <<< "${group_break}") \
    && echo "[INFO] Runing forces for ${group_name}" \
    && forces \
      --token "$(get_forces_token "${group_name}")" \
      -vvv \
      --repo-name "${repo_name}" \
      --"${kind}" \
      --"${strictness}"
}

main
