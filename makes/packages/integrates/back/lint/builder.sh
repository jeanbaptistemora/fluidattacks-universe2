# shellcheck shell=bash

function main {

  lint_python_package "${envIntegrates}/lambda" \
    && lint_python_package "${envIntegrates}/back/tests" \
    && lint_python_imports \
      "${envIntegratesImportsConfig}" \
      "${envIntegrates}/back/src" \
    && touch "${out}"
}

main "${@}"
