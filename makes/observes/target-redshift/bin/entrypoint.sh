# shellcheck shell=bash

source '__envBashLibPython__'

function main {
      make_python_path '3.7' \
        '__envTargetRedshift__' \
  &&  target-redshift "${@}"
}

main "${@}"
