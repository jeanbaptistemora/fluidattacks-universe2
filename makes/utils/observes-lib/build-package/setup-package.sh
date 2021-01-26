# shellcheck shell=bash

source '__envUtilsBashLibPython__'
source '__envSearchPaths__'

function __envPackageName___setup_runtime {
      make_python_path '3.8' \
        '__envPythonRequirements__'\
  &&  make_python_path_plain \
        '__envPackageSrc__'
}

__envPackageName___setup_runtime
