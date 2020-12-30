# shellcheck shell=bash

source '__envContextFile__'
source '__envUtilsBashLibPython__'

function skims_setup_runtime {
  export LD_LIBRARY_PATH="__envLibPath__:${LD_LIBRARY_PATH:-}"
  export PATH="__envBinPath__:${PATH:-}"
  export PYTHONPATH="__envPyPath__:${PYTHONPATH:-}"

      make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  make_python_path_plain \
        '__envSrcSkimsSkims__' \

}

function skims {
  '__envPython__' '__envSrcSkimsSkims__/cli/__init__.py' "$@"
}

skims_setup_runtime
