# shellcheck shell=bash

source '__envUtilsBashLibPython__'
source '__envSearchPaths__'

function streamer_zoho_crm_setup_runtime {
      make_python_path '3.8' \
        '__envPythonRequirements__'

}

function streamer_zoho_crm  {
  '__envPython__' '__envSrcObservesStreamerZohoCrmEntrypoint__' "$@"
}

streamer_zoho_crm_setup_runtime
