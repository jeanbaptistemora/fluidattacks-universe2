# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function melts_setup_runtime {
  # Leave melts use the host's home in order to allow credentials to live
  # many hours
  export HOME
  export HOME_IMPURE

      if test -n "${HOME_IMPURE:-}"
      then
        HOME="${HOME_IMPURE}"
      fi \
  &&  make_python_path '3.8' \
        '__envPythonRequirements__' \
  &&  make_python_path_plain \
        '__envSrcMelts__' \

}

function melts {
  '__envPython__' '__envSrcMelts__/toolbox/cli/__init__.py' "$@"
}

melts_setup_runtime
