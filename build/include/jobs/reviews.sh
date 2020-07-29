# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"

declare -Arx REVIEWS_GLOBAL_PKGS=(
  [cli]=src/cli
  [core]=src/core
  [utils]=src/utils
)

function job_reviews_install {
  local path='reviews'

  helper_common_poetry_install "${path}"
}

function job_reviews_lint {
  local args_mypy=(
    --ignore-missing-imports
    --strict
  )
  local args_prospector=(
    --strictness veryhigh
  )
  local path='reviews'

      helper_common_poetry_install_deps "${path}" \
  &&  pushd reviews/ \
    &&  for pkg in "${REVIEWS_GLOBAL_PKGS[@]}"
        do
              echo "[INFO] Static type checking: ${pkg}" \
          &&  poetry run mypy "${args_mypy[@]}" "${pkg}" \
          ||  return 1
        done \
    &&  for pkg in "${REVIEWS_GLOBAL_PKGS[@]}"
        do
              echo "[INFO] Linting: ${pkg}" \
          &&  poetry run prospector "${args_prospector[@]}" "${pkg}" \
          ||  return 1
        done \
  &&  popd \
  ||  return 1
}

function job_reviews_structure {
  local pydeps_args=(
    --cluster
    --include-missing
    --max-bacon 0
    --max-cluster-size 100
    --noshow
    --only "${!REVIEWS_GLOBAL_PKGS[@]}"
    --reverse
    -x 'click'
    --
    "${REVIEWS_GLOBAL_PKGS[cli]}"
  )
  local path='reviews'

      helper_common_poetry_install_deps "${path}" \
  &&  pushd reviews/ \
    &&  poetry run pydeps "${pydeps_args[@]}" \
  &&  popd \
  ||  return 1
}
