# shellcheck shell=bash

function main {
  if test -n "${UNIVERSE_API_TOKEN:-}"; then
    pushd "__argSrc__" \
      && go run main.go \
      && popd \
      || return 1
  else
    error "UNIVERSE_API_TOKEN must be set."
  fi
}

main "${@}"
