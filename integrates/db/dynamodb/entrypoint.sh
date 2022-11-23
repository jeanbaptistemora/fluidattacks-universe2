# shellcheck shell=bash

function main {
  : \
    && data-for-db \
    && dynamodb-for-db \
    || return 1
}

main "${@}"
