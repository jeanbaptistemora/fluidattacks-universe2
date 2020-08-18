# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"
source "${srcIncludeCommonJobs}"
source "${srcIncludeForcesJobs}"
source "${srcIncludeIntegratesJobs}"
source "${srcIncludeIntegratesLintersJobs}"
source "${srcIncludeSkimsJobs}"
source "${srcIncludeReviewsJobs}"

function cli {
  local function_to_call
  local arguments_1

  function_to_call="${1:-}"
  arguments_1="${2:-}"

  if test -z "${function_to_call}" \
      || test "${function_to_call}" = '-h' \
      || test "${function_to_call}" = '--help'
  then
    echo
    echo "Use: ./build.sh [job-name]"
    echo
    echo 'List of jobs:'
    helper_list_declared_jobs | sed -e 's/^/  * /g'
    return 0
  fi

  echo '---'
  env_prepare_environment_variables "${function_to_call}"
  env_prepare_ephemeral_vars
  echo "[INFO] Executing function: job_${function_to_call} ${arguments_1}"
  if "job_${function_to_call}" "${arguments_1}"
  then
    echo
    echo "Successfully executed: ${function_to_call} ${arguments_1}"
    echo '  Congratulations!'
    return 0
  else
    echo
    echo 'We have found some problems :('
    echo '  You can replicate this by running:'
    echo "    integrates $ ./build.sh ${function_to_call}"
    return 1
  fi
}
