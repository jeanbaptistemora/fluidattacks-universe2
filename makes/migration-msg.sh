#! /usr/bin/env bash
# shellcheck disable=SC2028

set -o pipefail
set -o nounset
set -o errexit

function loc {
  tokei "${1}" \
    | grep -P '^ Total' \
    | sed -E 's|^ Total\s+[0-9]+\s+[0-9]+\s+([0-9]+).*$|\1|g'
}

function main {
  : && start_loc='66327' \
    && start_seconds="$(date --date=2021-09-29 +%s)" \
    && end_seconds="$(date +%s)" \
    && elapsed_days="$(((end_seconds - start_seconds) / 86400))" \
    && migrated_loc="$(loc makes/foss)" \
    && migrated_loc="$((migrated_loc - start_loc))" \
    && total_loc="$(loc makes)" \
    && total_loc="$((total_loc - start_loc))" \
    && remaining_loc="$((total_loc - migrated_loc))" \
    && speed="$((migrated_loc / elapsed_days))" \
    && eta="$((remaining_loc * elapsed_days / migrated_loc))" \
    && msg="
      melts\\refac(build): #5408 migrate to makes

      - Speed: ${migrated_loc} loc / ${elapsed_days} days = ${speed} loc/day
      - TODO: ${remaining_loc} loc
      - ETA: ${remaining_loc} / ${speed} = ${eta} days
    " \
    && git commit -m "${msg//      /}"
}

main "${@}"
