# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function forces_setup_wrapper {
      make_python_path '3.8' \
        '__envPythonRequirements__'
}

function forces {
  '__envPython__' '__envForces__' "$@"
}

forces_setup_wrapper
