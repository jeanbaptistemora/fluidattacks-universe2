# shellcheck shell=bash

function lint {
    observes_generic_lint "${envSrc}" \
||  (
          echo '[INFO] Please fix lint issues' \
      &&  return 1
    )
}

function format {
    observes-pkg-format \
||  (
          echo '[INFO] Please run formatter (observes.job.format-code)' \
      &&  return 1
    )
}

lint && format
