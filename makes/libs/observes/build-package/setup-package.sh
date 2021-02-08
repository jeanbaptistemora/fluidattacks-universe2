# shellcheck shell=bash

source '__envUtilsBashLibPython__'
source '__envSearchPaths__'


function setup_runtime {
      make_python_path '3.8' \
        '__envPythonReqs__'\
  &&  make_python_path_plain \
        '__envPackageSrc__'
}

setup_runtime
