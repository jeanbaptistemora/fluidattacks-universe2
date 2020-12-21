#! __envShell__
# shellcheck shell=bash

# Setup the python path
export PYTHONPATH="__envPythonRequirements__:${PYTHONPATH:-}"
export PYTHONPATH="__envSrcSkimsSkims__:${PYTHONPATH:-}"
export PYTHONPATH="__envSrcSkimsStatic__:${PYTHONPATH:-}"
export PYTHONPATH="__envSrcSkimsVendor__:${PYTHONPATH:-}"

# Export pre-compiled binaries
export SKIMS_ANTLR='__envANTLR__/build/install/parse/bin/parse'

# Invoke the entrypoint
'__envPython__' '__envSrcSkimsSkims__/cli/__init__.py' "${@}"
