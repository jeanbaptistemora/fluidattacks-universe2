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
    return 0
  fi

  echo
  prepare_environment_variables
  prepare_ephemeral_vars
  prepare_workdir
  prepare_python_packages

  if test "${function_to_call}" = 'all'
  then
        job_lint_code \
    &&  job_infra_autoscaling_ci_test \
    &&  job_infra_aws_sso_test \
    &&  job_infra_monolith_test \
    &&  job_run_break_build_static \
    &&  job_run_break_build_dynamic \
    &&  job_user_provision_continuous_prod_test \
    &&  job_user_provision_continuous_dev_test \
    &&  job_user_provision_continuous_prod_test \
    &&  job_user_provision_integrates_dev_test \
    &&  job_user_provision_integrates_prod_test \
    &&  job_user_provision_web_prod_test \

  else
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
