# shellcheck shell=bash

function main {
  lint_python_imports \
    "${envIntegratesImportsConfig}" \
    "${envIntegrates}/back/src" \
    && touch "${out}"
}

main "${@}"
