# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function forces_setup_runtime {
      make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  make_python_path_plain \
        '__envSrcForces__'
}

function forces {
  '__envPython__' '__envSrcForces__/forces/cli/__init__.py' "$@"
}

forces_setup_runtime
