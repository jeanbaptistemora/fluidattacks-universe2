# shellcheck shell=bash

function helper_airs_generic_forbidden_extensions {
  local invalid_extensions='asc'
  local found_files

      found_files="$(find content/ -type f -regex  ".*\(${invalid_extensions}\)$")" \
  &&  if [ "${found_files}" == '' ]
      then
            return 0
      else
            echo '[ERROR] invalid/unsopported files found:' \
        &&  echo "${found_files}" \
        && return 1
      fi
}

function helper_airs_generic_file_name {
  local file="${1}"
  local regex='^[a-z0-9-]+\.[a-z0-9]+\.*[a-z0-9]*$'
  local filename

      helper_airs_file_exists "${file}" \
  &&  filename="$(basename "${file}")" \
  &&  if [[ ${filename} =~ ${regex} ]]
      then
            return 0
      else
            echo "[ERROR] ${filename} does not match the ${regex} convention" \
        &&  return 1
      fi
}
