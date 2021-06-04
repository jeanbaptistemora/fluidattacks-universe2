# shellcheck shell=bash

function main {
  local module="${1:-}"

  if test -n "${module}"; then
    lint_python_package "__envSrcSkimsSkims__/${module}"
  else
    lint_everything
  fi
}

function lint_everything {
  lint_python_imports '__envImportLinterConfig__' '__envSrcSkimsSkims__' \
    && lint_python_package '__envSrcSkimsTest__' \
    && lint_python_package '__envSrcProcessGroup__' \
    && lint_python_package '__envSrcTestMocksHttp__' \
    && lint_python_package '__envSrcSkimsTestSdk__' \
    && for module in "__envSrcSkimsSkims__/"*; do
      if test -d "${module}"; then
        lint_python_package "${module}"
      fi \
        || return 1
    done
}

main "${@}"
