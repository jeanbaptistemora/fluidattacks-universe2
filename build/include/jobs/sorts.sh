# shellcheck shell=bash

declare -Arx SORTS_GLOBAL_PKGS=(
  [cli]=sorts/cli
  [integrates]=sorts/integrates
  [predict]=sorts/predict
  [training]=sorts/training
  [utils]=sorts/utils
)

declare -Arx SORTS_GLOBAL_TEST_PKGS=(
  [test]=test/
)

function job_sorts_lint {
  local args_mypy=(
    --config-file 'settings.cfg'
  )
  local args_prospector=(
    # Some day when sorts has https://readthedocs.org
    # --doc-warnings
    --full-pep8
    --strictness veryhigh
    --test-warnings
  )

      helper_sorts_install_dependencies \
  &&  pushd sorts \
    &&  echo '[INFO] Checking static typing' \
    &&  poetry run mypy "${args_mypy[@]}" sorts/ \
    &&  poetry run mypy "${args_mypy[@]}" test/ \
    &&  echo "[INFO] Linting" \
    &&  poetry run prospector "${args_prospector[@]}" sorts/ \
    &&  poetry run prospector "${args_prospector[@]}" test/ \
  &&  popd \
  ||  return 1
}

function job_sorts_test {
  export PYTHONUNBUFFERED='1'
  local args_pytest=(
    --capture tee-sys
    --cov-branch
    --cov-report 'term'
    --cov-report "html:${PWD}/sorts/coverage/"
    --cov-report "xml:${PWD}/sorts/coverage.xml"
    --disable-pytest-warnings
    --exitfirst
    --no-cov-on-fail
    --reruns 3
    --show-capture no
    --verbose
  )

      helper_sorts_install_dependencies \
  &&  pushd sorts \
    &&  for pkg in "${SORTS_GLOBAL_PKGS[@]}" "${SORTS_GLOBAL_TEST_PKGS[@]}"
        do
          args_pytest+=( "--cov=${pkg}" )
        done \
    &&  poetry run pytest "${args_pytest[@]}" < /dev/null \
  &&  popd \
  ||  return 1
}

function job_sorts_deploy_to_pypi {
  # Propagated from Gitlab env vars
  export PYPI_TOKEN
  local version

  function restore_version {
    sed --in-place 's|^version.*$|version = "1.0.0"|g' "sorts/pyproject.toml"
  }

      helper_sorts_install_dependencies \
  &&  pushd sorts \
    &&  version=$(helper_common_poetry_compute_version) \
    &&  echo "[INFO] Sorts: ${version}" \
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
