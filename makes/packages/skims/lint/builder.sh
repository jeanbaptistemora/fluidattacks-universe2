# shellcheck shell=bash

function main {
      lint_python_imports "${envImportLinterConfig}" "${envSrcSkimsSkims}" \
  &&  lint_python_module "${envSrcSkimsTest}" \
  &&  for module in "${envSrcSkimsSkims}"/*
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
