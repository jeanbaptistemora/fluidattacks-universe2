# shellcheck shell=bash

source '__envSetupSkimsRuntime__'

function main {
      pushd skims \
    &&  __envPython__ "${@}" \
  &&  popd \
  ||  return 1
}

main "${@}"
