# shellcheck shell=bash

function observes_generic_runner {
  local entrypoint="${1}"
  python -c "${entrypoint} as entrypoint; entrypoint()" "${@:2}"
}
