# shellcheck shell=bash

function main {
  bandit --recursive "${envSrcIntegratesBack}" \
    --exclude tests \
    && touch "${out}"
}

main "${@}"
