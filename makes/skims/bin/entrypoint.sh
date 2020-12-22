#! __envShell__
# shellcheck shell=bash

# Setup the path
export PATH="__envRuntimeBinPath__:${PATH:-}"

# Setup linked path
export LD_LIBRARY_PATH="__envRuntimeLibPath__:${LD_LIBRARY_PATH:-}";

# Setup the python path
export PYTHONPATH="__envPythonRequirements__:${PYTHONPATH:-}"
export PYTHONPATH="__envSrcSkimsSkims__:${PYTHONPATH:-}"

# Context artifacts
source '__envContextFile__'

# Invoke the entrypoint
'__envPython__' '__envSrcSkimsSkims__/cli/__init__.py' "${@}"
