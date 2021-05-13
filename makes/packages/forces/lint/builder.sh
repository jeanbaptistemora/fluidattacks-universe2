# shellcheck shell=bash

function main {
      lint_python_package "${envSrcForcesForces}" \
  &&  lint_python_package "${envSrcForcesTest}" \
  &&  touch "${out}"
}

main "${@}"
