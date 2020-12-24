#! __envShell__
# shellcheck shell=bash

# Context artifacts
source '__makeEntrypoint__'
source '__envContextFile__'
source '__envUtilsBashLibPython__'

function main {
  export PATH="__envRuntimeBinPath__:${PATH:-}"
  export LD_LIBRARY_PATH='__envRuntimeLibPath__'

      unset PYTHONPATH \
  &&  make_python_path '3.8' \
      '__envPythonRequirements__' \
  &&  make_python_path_plain \
      '__envSrcSkimsSkims__' \
  &&  '__envPython__' '__envSrcSkimsSkims__/cli/__init__.py' "${@}"
}

main "${@}"
