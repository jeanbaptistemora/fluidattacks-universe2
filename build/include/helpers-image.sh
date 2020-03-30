# shellcheck shell=bash

source "${srcIncludeHelpers}"

function helper_image_blog_cover_dimensions {
  local path="${1}"
  local dimensions

      helper_file_exists "${path}" \
  &&  dimensions="$(identify -format "%wx%h" "${path}")" \
  &&  if [ "${dimensions}" = '600x280' ]
      then
            return 0
      else
            echo "[ERROR] ${path} does not have a size of 600x280" \
        && return 1
      fi
}

function helper_image_optimized {
  local path="${1}"

      helper_file_exists "${path}" \
  &&  if optipng -simulate "${path}" 2>&1 | tail -n2 | grep -q 'already optimized.'
      then
            return 0
      else
            echo "[ERROR] ${path} is not optimized" \
        &&  return 1
      fi
}

function helper_image_size {
  local path="${1}"
  local size_bytes

      helper_file_exists "${path}" \
  &&  size_bytes="$(stat -c %s "${path}")" \
  &&  if [ "${size_bytes}" -le '1000000' ]
      then
            return 0
      else
            echo "[ERROR] ${path} size is over 1mb" \
        &&  return 1
      fi
}

function helper_image_valid {
  local path="${1}"
  local valid_extensions='image/\(png\|svg+xml\|gif\)'

      helper_file_exists "${path}" \
  &&  if file --mime-type "${path}" | grep -q "${valid_extensions}"
      then
            return 0
      else
            echo "[ERROR] ${path} must be a valid format: ${valid_extensions}" \
        &&  return 1
      fi
}
