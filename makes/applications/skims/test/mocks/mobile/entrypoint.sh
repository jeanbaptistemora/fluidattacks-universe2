# shellcheck shell=bash

function main {
  export STATE

  mkdir -p "state" \
    && copy "__envAndroguardRepository__/examples" "${STATE}/android"
}

main "${@}"
