# shellcheck shell=bash

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
