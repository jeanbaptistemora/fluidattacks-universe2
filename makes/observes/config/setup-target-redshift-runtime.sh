# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function target_redshift_setup_runtime {
  export LD_LIBRARY_PATH="__envLibPath__:${LD_LIBRARY_PATH:-}"
  export PATH="__envBinPath__:${PATH:-}"
  export PYTHONPATH="__envPyPath__:${PYTHONPATH:-}"

      make_python_path '3.7' \
        '__envPythonRequirements__'

}

function target_redshift {
  '__envPython__' '__envSrcObservesTargetRedshiftEntrypoint__' "$@"
}

target_redshift_setup_runtime
