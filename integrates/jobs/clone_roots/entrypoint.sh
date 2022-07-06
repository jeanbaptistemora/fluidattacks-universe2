# shellcheck shell=bash

function main {
  source __argPythonEnv__/template \
    && python3 __argScript__

}

main "${@}"
