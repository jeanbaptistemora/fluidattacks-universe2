# shellcheck shell=bash

function main {
  local valid_extensions='image/\(png\|svg+xml\|gif\)'

      find "${envAirs}" -type f -exec file --mime-type {} + \
        | grep -oP '.*(?=:\s+image/)' > files \
  &&  while read -r path
      do
        if ! (file --mime-type "${path}" | grep -q "${valid_extensions}")
        then
          abort "[ERROR] ${path} must be a valid format: ${valid_extensions}"
        fi
      done < files \
  &&  touch "${out}"
}

main "${@}"
