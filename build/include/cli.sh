# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpers}"
source "${srcIncludeJobs}"

function cli {
  local function_to_call

  function_to_call="${1:-}"

  if test -z "${function_to_call}"
  then
    echo
    echo "Use: ./build.sh [job-name]"
    echo
    echo 'List of jobs:'
    helper_list_declared_jobs | sed -e 's/^/  * /g'
    return 1
  elif test "${function_to_call}" = 'all'
  then
    helper_list_declared_jobs \
      | while read -r func
        do
          echo "[INFO] Executing function: ${func}"
          cli "${func}" || return 1
        done
  else
    echo
    prepare_environment_variables
    prepare_ephemeral_vars
    prepare_workdir
    prepare_python_packages
    echo "[INFO] Executing function: job_${function_to_call}"
    if "job_${function_to_call}"
    then
      echo
      echo "Successfully executed: ${function_to_call}"
      echo '  Congratulations!'
      return 0
    else
      echo
      echo 'We have found some problems with your commit'
      echo '  You can replicate this output locally with:'
      echo "    serves $ ./build.sh ${function_to_call}"
      return 1
    fi
  fi
}
