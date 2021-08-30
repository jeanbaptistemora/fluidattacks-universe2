# shellcheck shell=bash

function main {
  lint_python_package "${envSrcMeltsTest}" \
    && touch "${out}"
}

main "${@}"
