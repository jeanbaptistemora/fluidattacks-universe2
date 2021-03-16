# shellcheck shell=bash

function main {
      bandit --recursive "${envSrcIntegratesBack}" \
  || true \
  &&  touch "${out}"
}

main "${@}"
