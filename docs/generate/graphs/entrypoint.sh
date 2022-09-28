# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local src="docs/src/docs"

  find "${src}" -type f -name '*.dot' | while read -r path; do
    : && info "Convering ${path} to SVG" \
      && dot -v \
      && if ! dot -O -Tsvg "${path}"; then
        critical "Failed to convert to SVG: ${path}"
      fi
  done
}

main "${@}"
