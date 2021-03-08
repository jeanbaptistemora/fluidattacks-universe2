# shellcheck shell=bash

function job_common_bugsnag_report {
      export PYTHONPATH=${PYTHONPATH:-}
      env_prepare_python_packages \
  &&  python3 "${STARTDIR}/common/bugsnag-report.py" "${@}"
}
