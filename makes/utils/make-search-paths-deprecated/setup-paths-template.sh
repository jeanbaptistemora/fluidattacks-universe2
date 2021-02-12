# shellcheck shell=bash

function setup {
  export LD_LIBRARY_PATH="__envLibPath__:${LD_LIBRARY_PATH:-}"
  export NODE_PATH="__envNodePath__:${NODE_PATH:-}"
  export PATH="__envBinPath__:__envNodePath__/.bin:${PATH:-}"
  export PYTHONPATH="__envPyPath__:${PYTHONPATH:-}"

}

setup
