# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function streamer_zoho_crm_setup_runtime {
  export LD_LIBRARY_PATH="__envLibPath__:${LD_LIBRARY_PATH:-}"
  export PATH="__envBinPath__:${PATH:-}"
  export PYTHONPATH="__envPyPath__:${PYTHONPATH:-}"

      make_python_path '3.8' \
        '__envPythonRequirements__'

}

function streamer_zoho_crm  {
  '__envPython__' '__envSrcObservesStreamerZohoCrmEntrypoint__' "$@"
}

streamer_zoho_crm_setup_runtime
