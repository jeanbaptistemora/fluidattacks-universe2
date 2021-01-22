# shellcheck shell=bash

source '__envUtilsBashLibPython__'
source '__envSearchPaths__'

function melts_setup_runtime {
      make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  make_python_path_plain \
        '__envSrcMelts__' \

}

function melts {
  '__envPython__' '__envSrcMelts__/toolbox/cli/__init__.py' "$@"
}

melts_setup_runtime
