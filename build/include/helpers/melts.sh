# shellcheck shell=bash

function helper_test_lint_code_python {
  local args_prospector=(
    --full-pep8
    --strictness veryhigh
    --test-warnings
  )
  local args_mypy=(
    --allow-any-generics
    --ignore-missing-imports
    --strict
  )

      pushd melts \
  &&  echo '[INFO]: Checking static typing...' \
  &&  mypy "${args_mypy[@]}" toolbox/sorts \
  &&  echo '[INFO]: Linting...' \
  &&  prospector "${args_prospector[@]}" toolbox/ \
  &&  popd \
  || return 0
}
