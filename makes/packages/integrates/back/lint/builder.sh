# shellcheck shell=bash

function main {
      for module in "${envIntegratesBackModules}"/*
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
