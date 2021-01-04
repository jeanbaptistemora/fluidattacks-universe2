# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function melts_setup_runtime {
  export LD_LIBRARY_PATH="__envLibPath__:${LD_LIBRARY_PATH:-}"
  export PATH="__envBinPath__:${PATH:-}"
  export PYTHONPATH="__envPyPath__:${PYTHONPATH:-}"

      make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  make_python_path_plain \
        '__envSrcMelts__' \

}

function melts {
  '__envPython__' '__envSrcMelts__/toolbox/cli/__init__.py' "$@"
}

melts_setup_runtime
