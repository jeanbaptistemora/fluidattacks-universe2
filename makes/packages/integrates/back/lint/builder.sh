# shellcheck shell=bash

function main {
      lint_python_module "${envIntegratesSrc}/back/packages/integrates-back/events" \
  &&  touch "${out}"
}

main "${@}"
