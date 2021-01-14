# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function sorts_setup_runtime {
  export LD_LIBRARY_PATH="__envLibPath__:${LD_LIBRARY_PATH:-}"
  export PATH="__envBinPath__:${PATH:-}"
  export PYTHONPATH="__envPyPath__:${PYTHONPATH:-}"

      make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  make_python_path_plain \
        '__envSrcSortsSorts__' \

}

function sorts {
  '__envPython__' '__envSrcSortsSorts__/cli/execute_sorts.py' "$@"
}

sorts_setup_runtime
