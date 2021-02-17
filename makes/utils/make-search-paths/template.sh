# shellcheck disable=SC2043 shell=bash

function with_library {
  export LD_LIBRARY_PATH="${1}/lib:${LD_LIBRARY_PATH:-}"
}

function with_node_library {
  export NODE_PATH="${1}:${NODE_PATH:-}"
}

function with_node_binary {
  export PATH="${1}/node_modules/.bin:${PATH:-}"
}

function with_path {
  export PATH="${1}/bin:${PATH:-}"
}

function with_python_path {
  export PYTHONPATH="${1}:${PYTHONPATH:-}"
}

function with_python37_path {
  export PYTHONPATH="${1}/lib/python3.7/site-packages:${PYTHONPATH:-}"
}

function with_python38_path {
  export PYTHONPATH="${1}/lib/python3.8/site-packages:${PYTHONPATH:-}"
}

function with_source {
  source "${1}"
}

function setup {
      for elem in __envLibraries__; do with_library "${elem}"; done \
  &&  for elem in __envNodeBinaries__; do with_node_binary "${elem}"; done \
  &&  for elem in __envNodeLibraries__; do with_node_library "${elem}"; done \
  &&  for elem in __envPaths__; do with_path "${elem}"; done \
  &&  for elem in __envPythonPaths__; do with_python_path "${elem}"; done \
  &&  for elem in __envPython37Paths__; do with_python37_path "${elem}"; done \
  &&  for elem in __envPython38Paths__; do with_python38_path "${elem}"; done \
  &&  for elem in __envSources__; do with_source "${elem}"; done \
  &&  for elem in __envUtils__; do with_source "${elem}"; done \

}

setup
