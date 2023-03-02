# shellcheck shell=bash

function main {
  export DATA
  export SCHEMA

  : \
    && DATA="$(cat "__argData__")" \
    && python "__argSrc__"
}

main "${@}"
