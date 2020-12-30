# shellcheck shell=bash

declare -Arx SKIMS_GLOBAL_PKGS=(
  [aws]=skims/aws
  [benchmark]=skims/benchmark
  [cli]=skims/cli
  [config]=skims/config
  [core]=skims/core
  [eval_java]=skims/eval_java
  [graph_java]=skims/graph_java
  [integrates]=skims/integrates
  [lib_path]=skims/lib_path
  [nvd]=skims/nvd
  [parse_antlr]=skims/parse_antlr
  [parse_babel]=skims/parse_babel
  [parse_cfn]=skims/parse_cfn
  [parse_common]=skims/parse_common
  [parse_hcl2]=skims/parse_hcl2
  [parse_java_properties]=skims/parse_java_properties
  [parse_json]=skims/parse_json
  [serialization]=skims/serialization
  [state]=skims/state
  [utils]=skims/utils
  [zone]=skims/zone
)

declare -Arx SKIMS_GLOBAL_TEST_PKGS=(
  [test]=test/
)

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
  &&  helper_common_list_services_groups "${groups_file}" \
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
  local vcpus='4'
  local memory='14400'
  local attempts='1'
  local timeout='18000'
  local group="${1}"
  local jobqueue='default'

      if [ -n "${SKIMS_GROUP_TO_PROCESS_ON_AWS:-}" ]
      then
            # This job was triggered from Integrates
            group="${SKIMS_GROUP_TO_PROCESS_ON_AWS}" \
        &&  jobqueue="asap"
      fi \
  &&  if test -z "${group}"
      then
            echo '[INFO] Please set the first argument to the group name' \
        &&  return 1
      fi \
  &&  jobname="skims_process_group__${group}" \
  &&  helper_skims_aws_login prod \
  &&  helper_common_run_on_aws \
        "${vcpus}" \
        "${memory}" \
        "${attempts}" \
        "${timeout}" \
        "${jobname}" \
        "${jobqueue}" \
        'skims_process_group' "${group}"
}

function job_skims_process_all_groups_on_aws {
  local groups_file="${TEMP_FILE1}"
  local groups_count

      echo '[INFO] Computing groups list' \
  &&  helper_common_list_services_groups "${groups_file}" \
  &&  groups_count=$(wc -l < "${groups_file}") \
  &&  echo "[INFO] ${groups_count} groups found" \
  &&  while read -r group
      do
            echo "[INFO] Submitting: ${group}" \
        &&  job_skims_process_group_on_aws "${group}" \
        ||  return 1
      done < "${groups_file}"
}

function job_skims_deploy_to_pypi {
  # Propagated from Gitlab env vars
  local version

  function restore_version {
    sed --in-place 's|^version.*$|version = "1.0.0"|g' "skims/pyproject.toml"
  }

      helper_skims_compile_parsers \
  &&  helper_skims_install_dependencies \
  &&  env_prepare_node_modules \
  &&  pushd skims \
    &&  version=$(helper_common_poetry_compute_version) \
    &&  echo "[INFO] Skims: ${version}" \
    &&  bugsnag-build-reporter \
          --api-key 'f990c9a571de4cb44c96050ff0d50ddb' \
          --app-version "${version}" \
          --release-stage 'production' \
          --source-control-provider 'gitlab' \
          --source-control-repository 'https://gitlab.com/fluidattacks/product.git' \
          --source-control-revision "${CI_COMMIT_SHA}" \
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
      helper_skims_compile_parsers \
  &&  helper_common_poetry_install skims \

}
