# shellcheck shell=bash

source "${envUtilsLintPython}"
source "${envReviewsRuntime}"

function main {
      for module in "${envSrcReviews}"/*
      do
            if test -d "${module}"
            then
              lint_python_module "${module}"
            fi \
        ||  return 1
      done \
  &&  touch "${out}"
}

main "${@}"
