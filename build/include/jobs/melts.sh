# shellcheck shell=bash

source "${srcIncludeHelpersMelts}"
source "${srcEnv}"

function job_melts_lint_code {
      env_prepare_python_packages \
  &&  helper_test_lint_code_python
}
