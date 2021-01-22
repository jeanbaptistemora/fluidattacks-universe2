# shellcheck shell=bash

source '__envSearchPaths__'
source '__envUtilsBashLibPython__'

function skims_setup_development {
      make_python_path '3.8' \
        '__envPythonRequirements__' \

}

skims_setup_development
