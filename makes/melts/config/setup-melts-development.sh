# shellcheck shell=bash

source '__envUtilsBashLibPython__'
source '__envSearchPaths__'

function melts_setup_development {
      make_python_path '3.8' \
        '__envPythonRequirements__'
}

melts_setup_development
