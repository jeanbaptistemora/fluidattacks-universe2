# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"

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
