# shellcheck shell=bash

function helper_airs_image_optimized {
  local path="${1}"

      helper_airs_file_exists "${path}" \
  &&  if optipng -simulate -o7 -zm1-9 "${path}" 2>&1 | tail -n2 | grep -q 'already optimized.'
      then
            return 0
      else
            echo "[ERROR] ${path} is not optimized" \
        &&  return 1
      fi
}

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
