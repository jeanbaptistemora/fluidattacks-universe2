# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"
source "${srcIncludeHelpersForces}"

function job_forces_lint {
  args_mypy=(
    --ignore-missing-imports
    --strict
  )
  args_prospector=(
    --strictness veryhigh
  )

  pushd forces/ \
  &&  { test -e forces/poetry.lock || poetry install; } \
  &&  echo "[INFO] Linting: Forces" \
  &&  poetry run mypy "${args_mypy[@]}"  "forces" \
  &&  poetry run prospector "${args_prospector[@]}" "forces" \
  ||  return 1 \
  &&  popd \
  ||  return 1
}


function job_forces_test {
  args_pytest=(
    --cov-branch
    --cov-fail-under '10'
    --cov-report 'term'
    --cov-report "html:${PWD}/skims/coverage/"
    --cov-report "xml:${PWD}/skims/coverage.xml"
    --disable-pytest-warnings
  )

      helper_forces_install_base_dependencies \
  &&  pushd forces/ \
    &&  args_pytest+=( "--cov=forces/" ) \
    &&  poetry run pytest "${args_pytest[@]}" \
  &&  popd \
  ||  return 1
}
