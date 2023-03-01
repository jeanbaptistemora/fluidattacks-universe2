# shellcheck shell=bash

function main {
  export SCHEDULES

  : \
    && SCHEDULES="$(cat "__argSchedules__")" \
    && python "__argSrc__"
}

main "${@}"
