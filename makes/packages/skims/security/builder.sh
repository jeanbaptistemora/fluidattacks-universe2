# shellcheck shell=bash

function main {
      bandit --recursive "${envSrcSkimsSkims}" \
  &&  touch "${out}"
}

main "${@}"
