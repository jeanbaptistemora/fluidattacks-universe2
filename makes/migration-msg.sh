#! /usr/bin/env bash

set -o pipefail
set -o nounset
set -o errexit

function loc {
  tokei "${1}" \
    | grep -P '^ Total' \
    | sed -E 's|^ Total\s+[0-9]+\s+[0-9]+\s+([0-9]+).*$|\1|g'
}

function main {
  local product="${1}"

  : && start_loc='66326' \
    && start_seconds="$(date --date=2021-09-29 +%s)" \
    && end_seconds="$(date +%s)" \
    && elapsed="$(((end_seconds - start_seconds) / 86400))" \
    && migrated="$(loc makes/foss)" \
    && migrated="$((migrated - start_loc))" \
    && total="$(loc makes)" \
    && total="$((total - start_loc))" \
    && remaining="$((total - migrated))" \
    && speed="$((migrated / elapsed))" \
    && eta="$((remaining * elapsed / migrated))" \
    && echo "
      ${product}\\refac(build): #5408 migrate to makes

      - Speed: ${migrated} loc / ${elapsed} days = ${speed} loc/day
      - TODO: ${remaining} loc
      - ETA: ${remaining} / ${speed} = ${eta} days
    "
}

main "${@}"
