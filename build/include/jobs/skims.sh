# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"
source "${srcIncludeHelpersSkims}"

declare -A GLOBAL_PKGS=(
  [cli]=src/cli
  [core]=src/core
  [integrates]=src/integrates
  [lib_path]=src/lib_path
  [utils]=src/utils
)

declare -A GLOBAL_TEST_PKGS=(
  [test]=test/
)

function job_skims_deploy {
  # Propagated from Gitlab env vars
  export SKIMS_PYPI_TOKEN
  local version
  local path='skims'

  function restore_version {
    sed --in-place 's|^version.*$|version = "1.0.0"|g' "skims/pyproject.toml"
  }

      helper_common_poetry_install_deps "${path}" \
  &&  pushd "${path}" \
    &&  version=$(helper_skims_compute_version) \
    &&  echo "[INFO] Skims: ${version}" \
    &&  trap 'restore_version' EXIT \
    &&  sed --in-place \
          "s|^version = .*$|version = \"${version}\"|g" \
          'pyproject.toml' \
    &&  poetry publish \
          --build \
          --password "${PYPI_TOKEN}" \
          --username '__token__' \
  &&  popd \
  ||  return 1
}

function job_skims_install {
  local path='skims'

  helper_common_poetry_install "${path}"
}

function job_skims_lint {
  local args_mypy=(
    --ignore-missing-imports
    --strict
  )
  local args_prospector=(
    --strictness veryhigh
  )
  local path='skims'

      helper_common_poetry_install_deps "${path}" \
  &&  pushd "${path}" \
    &&  for pkg in "${GLOBAL_PKGS[@]}" "${GLOBAL_TEST_PKGS[@]}"
        do
              echo "[INFO] Static type checking: ${pkg}" \
          &&  poetry run mypy "${args_mypy[@]}" "${pkg}" \
          ||  return 1
        done \
    &&  for pkg in "${GLOBAL_PKGS[@]}" "${GLOBAL_TEST_PKGS[@]}"
        do
              echo "[INFO] Linting: ${pkg}" \
          &&  poetry run prospector "${args_prospector[@]}" "${pkg}" \
          ||  return 1
        done \
  &&  popd \
  ||  return 1
}

function job_skims_structure {
  local pydeps_args=(
    --cluster
    --keep-target-cluster
    --max-bacon 0
    --max-cluster-size 100
    --noshow
    --only "${!GLOBAL_PKGS[@]}"
    --reverse
    -x 'click'
    --
    "${GLOBAL_PKGS[cli]}"
  )
  local path='skims'

      helper_common_poetry_install_deps "${path}" \
  &&  pushd "${path}" \
    &&  poetry run pydeps "${pydeps_args[@]}" \
  &&  popd \
  ||  return 1
}

function job_skims_test {
  local args_pytest=(
    --cov-branch
    --cov-fail-under '90'
    --cov-report 'term'
    --cov-report "html:${PWD}/skims/coverage/"
    --cov-report "xml:${PWD}/skims/coverage.xml"
    --disable-pytest-warnings
    --exitfirst
  )
  local path='skims'

      helper_common_poetry_install_deps "${path}" \
  &&  pushd "${path}" \
    &&  for pkg in "${GLOBAL_PKGS[@]}" "${GLOBAL_TEST_PKGS[@]}"
        do
          args_pytest+=( "--cov=${pkg}" )
        done \
    &&  poetry run pytest "${args_pytest[@]}" \
  &&  popd \
  ||  return 1
}
