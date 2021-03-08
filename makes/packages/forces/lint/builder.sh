# shellcheck shell=bash

function main {
      lint_python_module "${envSrcForcesForces}" \
  &&  lint_python_module "${envSrcForcesTest}" \
  &&  touch "${out}"
}

main "${@}"
