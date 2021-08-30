# shellcheck shell=bash

function main {
  lint_python_imports "${envImportLinterConfig}" "${envSrcSortsSorts}" \
    && touch "${out}"
}

main "${@}"
