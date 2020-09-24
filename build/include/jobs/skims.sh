# shellcheck shell=bash

declare -Arx SKIMS_GLOBAL_PKGS=(
  [aws]=skims/aws
  [cli]=skims/cli
  [config]=skims/config
  [core]=skims/core
  [integrates]=skims/integrates
  [lib_path]=skims/lib_path
  [nvd]=skims/nvd
  [parse_cfn]=skims/parse_cfn
  [parse_grammar]=skims/parse_grammar
  [parse_hcl2]=skims/parse_hcl2
  [parse_json]=skims/parse_json
  [serialization]=skims/serialization
  [state]=skims/state
  [utils]=skims/utils
  [zone]=skims/zone
)

declare -Arx SKIMS_GLOBAL_TEST_PKGS=(
  [test]=test/
)

function job_skims_documentation {
  local bucket_path='s3://web.fluidattacks.com/web/resources/doc/skims/'

      helper_skims_compile_ast \
  &&  helper_skims_install_dependencies \
  &&  pushd skims \
    &&  helper_skims_aws_login prod \
    &&  rm -rf docs/skims \
    &&  echo '[INFO] Building' \
    &&  poetry run pdoc \
          --force \
          --html \
          --output-dir docs/ \
          --template-dir docs/templates/ \
          skims \
    &&  aws s3 sync docs/skims/ "${bucket_path}" --delete \
    &&  rm -rf docs/skims/ \
  &&  popd \
  ||  return 1
}

function job_skims_dependencies_pack {
  helper_skims_dependencies_pack
}

function job_skims_dependencies_unpack {
  helper_skims_dependencies_unpack
}

function job_skims_process_group {
  local group="${1}"

  if test -n "${group}"
  then
        echo "[INFO] Processing: ${group}" \
    &&  helper_skims_process_group "${group}"
  else
        echo '[INFO] Please set the first argument to the group name' \
    &&  return 1
  fi
}

function job_skims_process_all_groups {
  local groups_file="${TEMP_FILE2}"
  local groups_count
  local success='true'

      echo '[INFO] Computing groups list' \
  &&  helper_list_services_groups "${groups_file}" \
  &&  groups_count=$(wc -l < "${groups_file}") \
  &&  echo "[INFO] ${groups_count} groups found" \
  &&  while read -r group
      do
            cd "${STARTDIR}" \
        &&  job_skims_process_group "${group}" \
        ||  success='false'
      done < "${groups_file}" \
  &&  test "${success}" = 'true' \
  ||  return 1
}

function job_skims_process_group_on_aws {
  local vcpus='2'
  local memory='7300'
  local attempts='1'
  local timeout='18000'
  export group="${1}"

      if test -z "${group}"
      then
            echo '[INFO] Please set the first argument to the group name' \
        &&  return 1
      fi \
  &&  helper_skims_aws_login prod \
  &&  helper_common_run_on_aws \
        "${vcpus}" \
        "${memory}" \
        "${attempts}" \
        "${timeout}" \
        'skims_process_group' "${group}"
}

function job_skims_process_all_groups_on_aws {
  local groups_file="${TEMP_FILE1}"
  local groups_count

      echo '[INFO] Computing groups list' \
  &&  helper_list_services_groups "${groups_file}" \
  &&  groups_count=$(wc -l < "${groups_file}") \
  &&  echo "[INFO] ${groups_count} groups found" \
  &&  while read -r group
      do
            echo "[INFO] Submitting: ${group}" \
        &&  job_skims_process_group_on_aws "${group}" \
        ||  return 1
      done < "${groups_file}"
}

function job_skims_deploy_infra {
      pushd skims \
    &&  helper_skims_aws_login prod \
    &&  helper_common_terraform_apply infra \
  &&  popd \
  ||  return 1
}

function job_skims_deploy_to_pypi {
  # Propagated from Gitlab env vars
  export SKIMS_PYPI_TOKEN
  local version

  function restore_version {
    sed --in-place 's|^version.*$|version = "1.0.0"|g' "skims/pyproject.toml"
  }

      helper_skims_compile_ast \
  &&  helper_skims_install_dependencies \
  &&  pushd skims \
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
      helper_skims_compile_ast \
  &&  helper_common_poetry_install skims \

}

function job_skims_lint {
  local args_mypy=(
    --config-file 'settings.cfg'
  )
  local args_prospector=(
    # Some day when skims has https://readthedocs.org !
    # --doc-warnings
    --full-pep8
    --strictness veryhigh
    --test-warnings
  )

      helper_skims_install_dependencies \
  &&  pushd skims \
    &&  echo '[INFO] Checking static typing' \
    &&  poetry run mypy "${args_mypy[@]}" skims/ \
    &&  poetry run mypy "${args_mypy[@]}" test/ \
    &&  echo "[INFO] Linting" \
    &&  poetry run prospector "${args_prospector[@]}" skims/ \
    &&  poetry run prospector "${args_prospector[@]}" test/ \
  &&  popd \
  ||  return 1
}

function job_skims_security {
  local bandit_args=(
    --recursive skims/
  )

      helper_skims_install_dependencies \
  &&  pushd skims \
    &&  poetry run bandit "${bandit_args[@]}" \
  &&  popd \
  ||  return 1
}

function job_skims_structure {
  local base_args=(
    --cluster
    --include-missing
    --max-bacon 0
    --noshow
    --only "${!SKIMS_GLOBAL_PKGS[@]}"
    --reverse
    -x 'click'
  )
  local end_args=(
    --
    "${SKIMS_GLOBAL_PKGS[cli]}"
  )

      helper_skims_install_dependencies \
  &&  pushd skims \
    &&  echo "[INFO]: Running pydeps" \
    &&  poetry run pydeps -o skims.file-dag.svg "${base_args[@]}" \
          --max-cluster-size 100 \
          "${end_args[@]}" \
    &&  poetry run pydeps -o skims.module-dag.svg "${base_args[@]}" \
          --max-cluster-size 1 \
          "${end_args[@]}" \
    &&  poetry run pydeps -o skims.cycles.svg "${base_args[@]}" \
          --max-cluster-size 100 \
          --show-cycles \
          "${end_args[@]}" \
  &&  popd \
  ||  return 1
}

function job_skims_test {
  export PYTHONUNBUFFERED='1'
  local args_pytest=(
    --capture tee-sys
    --cov-branch
    --cov-report 'term'
    --cov-report "html:${PWD}/skims/coverage/"
    --cov-report "xml:${PWD}/skims/coverage.xml"
    --disable-pytest-warnings
    --exitfirst
    --no-cov-on-fail
    --reruns 10
    --show-capture no
    --verbose
  )

      helper_skims_compile_ast \
  &&  helper_skims_install_dependencies \
  &&  pushd skims \
    &&  for pkg in "${SKIMS_GLOBAL_PKGS[@]}" "${SKIMS_GLOBAL_TEST_PKGS[@]}"
        do
          args_pytest+=( "--cov=${pkg}" )
        done \
    &&  poetry run pytest "${args_pytest[@]}" < /dev/null \
  &&  popd \
  ||  return 1
}

function job_skims_test_infra {
      pushd skims \
    &&  helper_skims_aws_login dev \
    &&  helper_common_terraform_plan infra \
  &&  popd \
  ||  return 1
}
