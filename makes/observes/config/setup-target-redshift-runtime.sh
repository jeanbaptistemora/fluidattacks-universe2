# shellcheck shell=bash

source '__envUtilsBashLibPython__'
source '__envSearchPaths__'

function target_redshift_setup_runtime {
      make_python_path '3.7' \
        '__envPythonRequirements__'

}

function target_redshift {
  '__envPython__' '__envSrcObservesTargetRedshiftEntrypoint__' "$@"
}

target_redshift_setup_runtime
