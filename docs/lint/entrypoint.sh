# shellcheck shell=bash

function main {
  : \
    && lint_npm_deps docs/src/package.json \
    || return 1
}

main "${@}"
