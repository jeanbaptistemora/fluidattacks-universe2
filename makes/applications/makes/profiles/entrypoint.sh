# shellcheck shell=bash

function dump {
  cat __envHacker__ > makes/profiles/hacker.sh
}

dump "${@}"
