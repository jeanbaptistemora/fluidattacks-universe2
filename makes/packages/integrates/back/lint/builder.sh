# shellcheck shell=bash

function main {
      lint_python_imports "${envIntegratesImportsConfig}" "${envIntegratesBackModules}" \
  &&  for module in "${envIntegratesBackModules}"/*
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
