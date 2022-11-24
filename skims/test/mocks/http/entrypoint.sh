# shellcheck shell=bash

function main {
  local host="${1:-localhost}"
  local port="${2:-48000}"

  pushd __argApp__ \
    && kill_port "${port}" \
    && flask run \
      --host "${host}" \
      --port "${port}" \
    && popd \
    || return 1
}

main "${@}"
