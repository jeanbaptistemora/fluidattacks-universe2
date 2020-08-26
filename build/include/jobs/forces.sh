# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersIntegrates}"
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
    --cov-fail-under '80'
    --cov-report 'term'
    --cov-report "html:${PWD}/forces/coverage/"
    --cov-report "xml:${PWD}/forces/coverage.xml"
    --disable-pytest-warnings
  )

      helper_forces_install_base_dependencies \
  &&  pushd forces/ \
    &&  args_pytest+=( "--cov=forces/" ) \
    &&  poetry run pytest "${args_pytest[@]}" \
  &&  popd \
  ||  return 1
}

function job_forces_deploy {
  # Propagated from Gitlab env vars
  export PYPI_TOKEN
  local version

  function restore_version {
    sed --in-place 's|^version.*$|version = "1.0.0"|g' "forces/pyproject.toml"
  }

      helper_forces_install_base_dependencies \
  &&  pushd forces/ \
    &&  version=$(helper_forces_compute_version) \
    &&  echo "[INFO] Forces: ${version}" \
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


function job_forces_deploy_to_docker_hub {
  local forces_image="fluidattacks/forces:new"
  local break_build_image="fluidattacks/break-build:new"

      helper_integrates_aws_login "${ENVIRONMENT_NAME}" \
  &&  sops_env "integrates/secrets-${ENVIRONMENT_NAME}.yaml" default \
        DOCKER_HUB_USER \
        DOCKER_HUB_PASS \
  &&  echo "[INFO] Logging in to Docker Hub" \
  &&  docker login "${DOCKER_HUB_URL}" \
      --username "${DOCKER_HUB_USER}" \
      --password-stdin \
      <<< "${DOCKER_HUB_PASS}" \
  && pushd forces \
    && docker build  \
          --tag "${forces_image}" \
          --target "forces" \
          -f "Dockerfile" \
          . \
    && docker build  \
          --tag "${break_build_image}" \
          --target "break_build" \
          -f "Dockerfile" \
          . \
    &&  docker push "${forces_image}" \
    &&  docker push "${break_build_image}" \
  && popd \
  || return 1
}
