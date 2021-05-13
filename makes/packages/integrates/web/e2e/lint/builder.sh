# shellcheck shell=bash

function main {
      lint_python_package "${envSrc}" \
  &&  touch "${out}"
}

main "${@}"
