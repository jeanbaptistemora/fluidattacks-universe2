# shellcheck shell=bash

source "${envSetupSkimsDevelopment}"

function main {
      bandit --recursive "${envSrcSkimsSkims}" \
  &&  touch "${out}"
}

main "${@}"
