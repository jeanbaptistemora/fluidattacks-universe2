# shellcheck shell=bash

source "${makeSetup}"

function replace_var_in_file {
  local file="${1}"
  local var_name="${2}"
  local var_value="${!var_name}"

      echo "[INFO] Replacing: __${var_name}__, with: ${var_value}" \
  &&  sed -i "s|__${var_name}__|${var_value}|g" "${file}"
}

function main {
      copy "${__envTemplate}" "${out}" \
  &&  while read -r 'var_name'
      do
            replace_var_in_file "${out}" "${var_name}" \
        ||  return 1
      done < "${__envArguments}" \
  &&  if test "${__envExecutable}" = 'true'
      then
        chmod +x "${out}"
      fi
}

main "${@}"
