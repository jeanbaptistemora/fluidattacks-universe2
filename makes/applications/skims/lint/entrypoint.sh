# shellcheck shell=bash

function main {
  lint_python_imports '__envImportLinterConfig__' '__envSrcSkimsSkims__'
}

main "${@}"
