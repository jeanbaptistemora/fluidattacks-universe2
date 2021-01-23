# shellcheck shell=bash

function sops_export_vars {
  local manifest="${1}"
  local profile="${2}"

      echo "[INFO] Decrypting ${manifest} with profile ${profile}" \
  &&  json=$( \
        '__envSops__' \
          --aws-profile "${profile}" \
          --decrypt \
          --output-type json \
          "${manifest}" \
      ) \
  &&  for var in "${@:3}"
      do
            echo "[INFO] Exported: ${var}" \
        &&  export "${var//./__}=$(echo "${json}" | '__envJq__' -r ".${var}")" \
        ||  return 1
      done
}
