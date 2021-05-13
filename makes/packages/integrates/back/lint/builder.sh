# shellcheck shell=bash

function main {

      lint_python_package "${envIntegratesBack}"/migrations \
  &&  lint_python_imports \
        "${envIntegratesImportsConfig}" \
        "${envIntegratesBack}/packages/modules" \
  &&  for module in "${envIntegratesBack}/packages/modules"/*
      do
            if test -d "${module}"
            then
              lint_python_package "${module}"
            fi \
        ||  return 1
      done \
  &&  touch "${out}"
}

main "${@}"
