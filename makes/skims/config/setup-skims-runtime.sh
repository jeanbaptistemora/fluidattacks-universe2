# shellcheck shell=bash

source '__envContextFile__'
source '__envUtilsBashLibPython__'

function skims_setup_runtime {
  export LD_LIBRARY_PATH='__envRuntimeLibPath__'
  export PATH="__envRuntimeBinPath__:${PATH:-}"

      make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  make_python_path_plain \
        '__envSrcSkimsSkims__' \

}

function skims {
  '__envPython__' '__envSrcSkimsSkims__/cli/__init__.py' "$@"
}

skims_setup_runtime
