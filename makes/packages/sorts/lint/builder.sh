# shellcheck shell=bash

function main {
  lint_python_imports "${envImportLinterConfig}" "${envSrcSortsSorts}" \
    && lint_python_package "${envSrcSortsTest}" \
    && lint_python_package "${envSrcSortsTraining}" \
    && touch "${out}"
}

main "${@}"
