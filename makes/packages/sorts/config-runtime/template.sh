# shellcheck shell=bash

source '__envSearchPaths__'
source '__envUtilsBashLibPython__'
source '__envContextFile__'

function sorts_setup_runtime {
      make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  make_python_path_plain \
        '__envSrcSortsSorts__'
}

function sorts {
  '__envPython__' '__envSrcSortsSorts__/cli/__init__.py' "$@"
}

sorts_setup_runtime
