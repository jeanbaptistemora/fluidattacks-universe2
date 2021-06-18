# shellcheck shell=bash

function main {
  lint_markdown "${envSrcDocs}" \
    && touch "${out}"
}

main "${@}"
