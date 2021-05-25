# shellcheck shell=bash

function main {

      lint_python_package "${envIntegrates}/back/migrations" \
  &&  prospector --profile "${envProspectorSettings}" "${envIntegrates}/lambda" \
  &&  prospector --profile "${envProspectorSettings}" "${envIntegrates}/deploy/permissions-matrix" \
  &&  prospector --profile "${envProspectorSettings}" "${envIntegrates}/back/tests" \
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
