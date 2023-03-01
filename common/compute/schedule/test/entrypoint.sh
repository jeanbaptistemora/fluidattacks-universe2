# shellcheck shell=bash

function main {
  export DATA

  : \
    && DATA="$(yq -rec "." "__argData__")" \
    && python "__argSrc__"
}

main "${@}"
