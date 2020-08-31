# shellcheck shell=bash

function helper_test_lint_code_python {
  local args_prospector=(
    --full-pep8
    --strictness veryhigh
    --test-warnings
  )

      pushd melts \
  &&  echo '[INFO]: Checking static typing...' \
  &&  mypy --ignore-missing-imports --strict toolbox/sorts \
  &&  echo '[INFO]: Linting...' \
  &&  prospector "${args_prospector[@]}" toolbox/ \
  &&  popd \
  || return 0
}
