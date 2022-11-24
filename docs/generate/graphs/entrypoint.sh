# shellcheck shell=bash

function main {
  local src="docs/src/docs"

  find "${src}" -type f -name '*.dot' | while read -r path; do
    : && info "Converting ${path} to SVG" \
      && if ! dot -O -Tsvg "${path}"; then
        critical "Failed to convert to SVG: ${path}"
      fi
  done
}

main "${@}"
