# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"
source "${srcIncludeHelpersSkims}"

GLOBAL_PKGS=(
  src/apis
  src/cli
  src/core
  test/
)

function job_skims_lint {
  args_mypy=(
    --ignore-missing-imports
    --strict
  )
  args_prospector=(
    --strictness veryhigh
  )

      helper_skims_install_dependencies \
  &&  pushd skims/ \
    &&  for pkg in "${GLOBAL_PKGS[@]}"
        do
              echo "[INFO] Static type checking: ${pkg}" \
          &&  poetry run mypy "${args_mypy[@]}" "${pkg}" \
          ||  return 1
        done \
    &&  for pkg in "${GLOBAL_PKGS[@]}"
        do
              echo "[INFO] Linting: ${pkg}" \
          &&  poetry run prospector "${args_prospector[@]}" "${pkg}" \
          ||  return 1
        done \
  &&  popd \
  ||  return 1
}

function job_skims_test {
  args_pytest=(
    --disable-pytest-warnings
  )

      helper_skims_install_dependencies \
  &&  pushd skims/ \
    &&  for pkg in "${GLOBAL_PKGS[@]}"
        do
          args_pytest+=( "--cov=${pkg}" )
        done \
    &&  poetry run pytest "${args_pytest[@]}" \
  &&  popd \
  ||  return 1
}

function job_skims_install {
  helper_skims_force_install
}
