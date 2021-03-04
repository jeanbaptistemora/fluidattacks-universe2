# shellcheck shell=bash

function helper_airs_image_size {
  local path="${1}"
  local size_bytes

      helper_airs_file_exists "${path}" \
  &&  size_bytes="$(stat -c %s "${path}")" \
  &&  if [ "${size_bytes}" -le '1000000' ]
      then
            return 0
      else
            echo "[ERROR] ${path} size is over 1mb" \
        &&  return 1
      fi
}
