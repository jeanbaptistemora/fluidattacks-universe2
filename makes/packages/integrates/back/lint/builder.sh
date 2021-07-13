# shellcheck shell=bash

function main {

  lint_python_package "${envIntegrates}/back/migrations" \
    && lint_python_package "${envIntegrates}/lambda" \
    && lint_python_package "${envIntegrates}/deploy/permissions_matrix" \
    && lint_python_package "${envIntegrates}/back/tests" \
    && lint_python_imports \
      "${envIntegratesImportsConfig}" \
      "${envIntegrates}/back/src" \
    && touch "${out}"
}

main "${@}"
