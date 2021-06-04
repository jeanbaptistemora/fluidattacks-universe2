# shellcheck shell=bash

function main {
      lint_markdown "${envSrcDocsDevelopment}" \
  &&  touch "${out}"
}

main "${@}"
