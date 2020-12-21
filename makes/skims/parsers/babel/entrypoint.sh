#! __envShell__
# shellcheck shell=bash

# Setup the path
export NODE_PATH="__envNodejsRequirements__/node_modules:${PYTHONPATH:-}"

# Invoke the entrypoint
'__envNodejs__' '__envSrc__/parse.js' "${@}"
