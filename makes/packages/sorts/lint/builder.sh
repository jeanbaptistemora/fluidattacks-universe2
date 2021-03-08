# shellcheck shell=bash

function main {
      lint_python_imports "${envImportLinterConfig}" "${envSrcSortsSorts}" \
  &&  lint_python_module "${envSrcSortsTest}" \
  &&  lint_python_module "${envSrcSortsTraining}" \
  &&  for module in "${envSrcSortsSorts}"/*
      do
            if test -d "${module}"
            then
              lint_python_module "${module}"
            fi \
        ||  return 1
      done \
  &&  touch "${out}"
}

main "${@}"
