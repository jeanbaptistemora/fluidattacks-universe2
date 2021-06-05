# shellcheck shell=bash

function main {
  lint_python_imports "${envImportLinterConfig}" "${envSrcSortsSorts}" \
    && lint_python_package "${envSrcSortsTest}" \
    && lint_python_package "${envSrcSortsTraining}" \
    && for module in "${envSrcSortsSorts}"/*; do
      if test -d "${module}"; then
        lint_python_package "${module}"
      fi \
        || return 1
    done \
    && touch "${out}"
}

main "${@}"
