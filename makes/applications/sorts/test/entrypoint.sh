# shellcheck shell=bash

function main {
  local args_pytest=(
      --capture tee-sys
      --cov-branch
      --cov-report 'term'
      --cov-report "html:${PWD}/sorts/coverage/"
      --cov-report "xml:${PWD}/sorts/coverage.xml"
      --disable-pytest-warnings
      --exitfirst
      --no-cov-on-fail
      --reruns 3
      --show-capture no
      --verbose
    )

  pushd sorts \
    &&  for pkg in '__envSrcSortsSorts__'/*
        do
          args_pytest+=( "--cov=${pkg}" )
        done \
    &&  pytest "${args_pytest[@]}" < /dev/null \
  &&  popd \
  ||  return 1
}

main "${@}"
