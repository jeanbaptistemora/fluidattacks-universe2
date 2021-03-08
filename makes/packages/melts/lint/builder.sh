# shellcheck shell=bash

function main {
      lint_python_module "${envSrcMeltsToolbox}" \
  &&  lint_python_module "${envSrcMeltsTest}" \
  &&  touch "${out}"
}

main "${@}"
