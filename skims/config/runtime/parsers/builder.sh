# shellcheck shell=bash

function main {
  export envBuildPy

  python "${envBuildPy}"
}

main "${@}"
