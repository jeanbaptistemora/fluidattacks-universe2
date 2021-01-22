# shellcheck shell=bash

source '__envUtilsBashLibPython__'
source '__envSearchPaths__'

function forces_setup_development {
      make_python_path '3.8' \
        '__envPythonRequirements__'
}

forces_setup_development
