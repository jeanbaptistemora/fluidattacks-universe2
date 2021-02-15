# shellcheck shell=bash

function sops_export_vars {
  sops_export_vars_by_profile "${1}" 'default' "${@:2}"
}

function sops_export_vars_by_profile {
  local manifest="${1}"
  local profile="${2}"

      echo "[INFO] Decrypting ${manifest} with profile ${profile}" \
  &&  json=$( \
        sops \
          --aws-profile "${profile}" \
          --decrypt \
          --output-type json \
          "${manifest}" \
      ) \
  &&  for var in "${@:3}"
      do
            echo "[INFO] Exported: ${var}" \
        &&  export "${var//./__}=$(echo "${json}" | jq -r ".${var}")" \
        ||  return 1
      done
}
