# shellcheck shell=bash

function main {
  mkdir -p "state" \
    && copy "__envAndroguardRepository__/examples" "state/android"
}

main "${@}"
