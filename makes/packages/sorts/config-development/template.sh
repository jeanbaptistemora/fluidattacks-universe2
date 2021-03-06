# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function sorts_setup_development {
      make_python_path '3.8' \
        '__envPythonRequirements__' \

}

sorts_setup_development
