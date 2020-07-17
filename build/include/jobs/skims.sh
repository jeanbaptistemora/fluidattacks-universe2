# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpers}"

function job_skims_lint {
  args_mypy=(
    --ignore-missing-imports
    --strict
  )
  args_prospector=(
    --strictness veryhigh
  )

      pushd skims/ \
    &&  { test -e poetry.lock || poetry install; } \
    &&  for pkg in \
          src/apis \
          src/cli \
          src/core \

        do
              echo "[INFO] Linting: ${pkg}" \
          &&  poetry run mypy "${args_mypy[@]}" "${pkg}" \
          &&  poetry run prospector "${args_prospector[@]}" "${pkg}" \
          ||  return 1
        done \
  &&  popd \
  ||  return 1
}
