# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"

function job_lint_forces {
      env_prepare_python_packages \
  &&  mypy --strict --ignore-missing-imports forces/ \
  &&  prospector --strictness verihigh forces/client/ \

}
