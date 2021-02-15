# shellcheck shell=bash

source "${srcEnv}"

source "${srcIncludeHelpersCommon}"
source "${srcIncludeHelpersCommonGitlab}"
source "${srcIncludeCommonJobs}"

source "${srcIncludeHelpersAirs}"
source "${srcIncludeHelpersAirsBlog}"
source "${srcIncludeHelpersAirsDeploy}"
source "${srcIncludeHelpersAirsGeneric}"
source "${srcIncludeHelpersAirsImage}"
source "${srcIncludeAirsJobs}"

source "${srcIncludeHelpersAsserts}"
source "${srcIncludeAssertsJobs}"

source "${srcIncludeHelpersIntegrates}"
source "${srcIncludeIntegratesJobs}"

source "${srcIncludeHelpersObserves}"
source "${srcIncludeObservesJobs}"

source "${srcIncludeReviewsJobs}"

source "${srcIncludeHelpersServices}"

function cli {
  local function_to_call="${1:-}"
  local arg1="${2:-}"
  local arg2="${3:-}"
  local arg3="${4:-}"
  local arg4="${5:-}"
  local arg5="${6:-}"
  local arg6="${7:-}"
  local arg7="${8:-}"

  if test -z "${function_to_call}" \
      || test "${function_to_call}" = '-h' \
      || test "${function_to_call}" = '--help'
  then
    echo
    echo "Use: ./build.sh [job-name]"
    echo
    echo 'List of jobs:'
    helper_common_list_declared_jobs "${arg1}" | sed -e 's/^/  * /g'
    return 0
  fi

  echo '---'
  env_prepare_environment_variables "${function_to_call}"
  env_prepare_ephemeral_vars

  if [[ $function_to_call == "common_bugsnag_report" ]]
  then
    shift
    arg1="$*"
  fi

  echo "[INFO] Executing function: job_${function_to_call} ${arg1} ${arg2} ${arg3} ${arg4} ${arg5} ${arg6} ${arg7}"
  if "job_${function_to_call}" "${arg1}" "${arg2}" "${arg3}" "${arg4}" "${arg5}" "${arg6}" "${arg7}"
  then
    echo
    echo "Successfully executed: ${function_to_call} ${arg1} ${arg2} ${arg3} ${arg4} ${arg5} ${arg6} ${arg7}"
    echo '  Congratulations!'
    return 0
  else
    echo
    echo 'We have found some problems :('
    echo '  You can replicate this by running:'
    echo "    product $ ./build.sh ${function_to_call}"
    return 1
  fi
}
