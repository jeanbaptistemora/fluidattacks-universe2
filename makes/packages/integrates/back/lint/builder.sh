# shellcheck shell=bash

function main {

      lint_python_package "${envIntegrates}/back/migrations" \
  &&  lint_python_package "${envIntegrates}/lambda" \
  &&  lint_python_package "${envIntegrates}/deploy/permissions_matrix" \
  &&  lint_python_package "${envIntegrates}/back/tests" || true \
  &&  lint_python_imports \
        "${envIntegratesImportsConfig}" \
        "${envIntegrates}/back/packages/modules" \
  &&  for module in "${envIntegrates}/back/packages/modules"/*
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
