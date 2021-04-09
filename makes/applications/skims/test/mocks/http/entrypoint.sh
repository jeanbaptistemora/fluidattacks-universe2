# shellcheck shell=bash

function main {
  local host="${1}"
  local port="${2}"

      pushd __envApp__ \
    &&  makes-kill-port "${port}" \
    &&  flask run \
          --host "${host}" \
          --port "${port}" \
  &&  popd \
  ||  return 1
}

main "${@}"
