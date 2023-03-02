# shellcheck shell=bash

function main {
  export DATA
  export SCHEMA

  : \
    && DATA="$(yq -rec "." "__argData__")" \
    && SCHEMA="$(cat "__argSchema__")" \
    && python "__argSrc__"
}

main "${@}"
