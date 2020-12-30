# shellcheck shell=bash

source "${makeDerivation}"
source "${envSetupSkimsDevelopment}"

function main {
      bandit --recursive "${envSrcSkimsSkims}" \
  &&  success
}

main "${@}"
