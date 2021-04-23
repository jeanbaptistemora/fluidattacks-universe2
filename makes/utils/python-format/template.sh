# shellcheck shell=bash

function main {
  if test -n "${CI:-}"
  then
    black '__envTarget__' \
      --config '__envSettingsBlack__' \
      --diff \
      --check \
      --color
  else
    black '__envTarget__' \
      --config '__envSettingsBlack__'
  fi
}

main "${@}"
