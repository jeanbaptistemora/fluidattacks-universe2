# shellcheck shell=bash

function main {
      for module in "${envSrcReviews}"/*
      do
            if test -d "${module}"
            then
              lint_python_package "${module}"
            fi \
        ||  return 1
      done \
  &&  touch "${out}"
}

main "${@}"
