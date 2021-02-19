# shellcheck shell=bash

function main {
      lint_python_module "${envSrc}" \
  &&  touch "${out}"
}

main "${@}"
