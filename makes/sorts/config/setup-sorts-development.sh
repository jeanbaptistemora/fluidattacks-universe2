# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function sorts_setup_development {
  export LD_LIBRARY_PATH="__envLibPath__:${LD_LIBRARY_PATH:-}"
  export PATH="__envBinPath__:${PATH:-}"
  export PYTHONPATH="__envPyPath__:${PYTHONPATH:-}"

      make_python_path '3.8' \
        '__envPythonRequirements__' \

}

sorts_setup_development
