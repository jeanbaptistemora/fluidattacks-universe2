# shellcheck shell=bash

declare -Arx SORTS_GLOBAL_PKGS=(
  [cli]=sorts/cli
  [features]=sorts/features
  [integrates]=sorts/integrates
  [predict]=sorts/predict
  [training]=sorts/training
  [utils]=sorts/utils
)

declare -Arx SORTS_GLOBAL_TEST_PKGS=(
  [test]=test/
)

function job_sorts_lint_code {
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

function job_sorts_test_code {
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

function job_sorts_test_infra {
  local target='infra'

      helper_common_use_pristine_workdir \
  &&  pushd sorts \
    &&  helper_sorts_aws_login dev \
    &&  helper_sorts_terraform_plan "${target}" \
  &&  popd \
  ||  return 1
}

function job_sorts_deploy_infra {
  local target='infra'

      helper_common_use_pristine_workdir \
  &&  pushd sorts \
    &&  helper_sorts_aws_login prod \
    &&  helper_common_terraform_apply "${target}" \
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

function job_sorts_extract_all_features_on_aws {
  local groups_file="${TEMP_FILE1}"
  local groups_count

      echo '[INFO] Computing groups list' \
  &&  helper_common_list_services_groups "${groups_file}" \
  &&  groups_count=$(wc -l < "${groups_file}") \
  &&  echo "[INFO] ${groups_count} groups found" \
  &&  while read -r group
      do
            echo "[INFO] Submitting: ${group}" \
        &&  job_sorts_extract_features_on_aws "${group}" \
        ||  return 1
      done < "${groups_file}"
}

function job_sorts_extract_features_on_aws {
  local vcpus='2'
  local memory='3600'
  local attempts='10'
  local timeout='18000'
  local group="${1}"
  local jobqueue='default'

      jobname="sorts_extract_features__${group}" \
  &&  helper_sorts_aws_login prod \
  &&  helper_common_run_on_aws \
        "${vcpus}" \
        "${memory}" \
        "${attempts}" \
        "${timeout}" \
        "${jobname}" \
        "${jobqueue}" \
        'sorts_extract_features' "${group}"
}

function job_sorts_extract_features {
  local group="${1}"

  if test -n "${group}"
  then
        echo "[INFO] Processing: ${group}" \
    &&  helper_sorts_extract_features "${group}"
  else
        echo '[INFO] Please set the first argument to the group name' \
    &&  return 1
  fi
}
