# shellcheck disable=SC2043 shell=bash

function with_library {
  export LD_LIBRARY_PATH="${1}/lib:${LD_LIBRARY_PATH:-}"
}

function with_node_path {
  export NODE_PATH="${1}:${NODE_PATH:-}"
  export PATH="${1}/.bin:${PATH:-}"
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

function setup {
      for elem in __envLibraries__; do with_library "${elem}"; done \
  &&  for elem in __envNodePaths__; do with_node_path "${elem}"; done \
  &&  for elem in __envPaths__; do with_path "${elem}"; done \
  &&  for elem in __envPythonPaths__; do with_python_path "${elem}"; done \
  &&  for elem in __envPython37Paths__; do with_python37_path "${elem}"; done \
  &&  for elem in __envPython38Paths__; do with_python38_path "${elem}"; done \

}

setup
