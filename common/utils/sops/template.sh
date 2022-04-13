# shellcheck shell=bash

function sops_export_vars {
  sops_export_vars_by_profile "${1}" 'default' "${@:2}"
}

function sops_export_vars_terraform {
  local manifest="${1}"
  local prefix="^${2}[_A-Z]+"
  local vars=()

  function get_vars {
    grep -oP "${prefix}" "${manifest}" | tr '\n' ' '
  }

  IFS=' ' read -ra vars <<< "$(get_vars)" \
    && sops_export_vars "${manifest}" \
      "${vars[@]}" \
    && for var in "${vars[@]}"; do
      export "TF_VAR_${var,,}=${!var}" \
        && echo "[INFO] Exported: TF_VAR_${var,,}" \
        || return 1
    done
}

function sops_export_vars_by_profile {
  local manifest="${1}"
  local profile="${2}"

  echo "[INFO] Decrypting ${manifest} with profile ${profile}" \
    && json=$(
      sops \
        --aws-profile "${profile}" \
        --decrypt \
        --output-type json \
        "${manifest}"
    ) \
    && for var in "${@:3}"; do
      echo "[INFO] Exported: ${var}" \
        && export "${var//./__}=$(echo "${json}" | jq -erc ".${var}")" \
        || return 1
    done
}
