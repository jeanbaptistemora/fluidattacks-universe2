# shellcheck shell=bash

function job_asserts_lint_code {
  local config_file='.pylintrc'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_config_precommit \
  &&  helper_common_list_touched_files | xargs pre-commit run -v --files \
  &&  prospector \
        --full-pep8 \
        --without-tool pep257 \
        --with-tool pyroma \
        --strictness veryhigh \
        --output-format text \
        --pylint-config-file="${config_file}" \
        fluidasserts/ \
  &&  popd \
  || return 1
}

function job_asserts_lint_code_bandit {
      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  bandit \
        -ii \
        -s B501,B601,B402,B105,B321,B102,B107,B307 \
        -r \
        fluidasserts \
  &&  popd \
  || return 1
}

function job_asserts_lint_tests {
  local config_file='.pylintrc'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  prospector \
        --full-pep8 \
        --without-tool pep257 \
        --with-tool pyroma \
        --strictness veryhigh \
        --output-format text \
        --pylint-config-file="${config_file}" \
        test/ \
  &&  popd \
  || return 1
}

function job_asserts_infra_secret_management_test {
  local target='deploy/secret-management/terraform'

      helper_use_pristine_workdir \
  &&  pushd asserts \
    &&  helper_asserts_aws_login dev \
    &&  helper_asserts_terraform_plan "${target}" \
  &&  popd \
  ||  return 1
}

function job_asserts_infra_secret_management_deploy {
  local dir='deploy/secret-management/terraform'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  helper_asserts_aws_login prod \
  &&  helper_common_terraform_apply "${dir}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_cloud_aws_api {
  local marker_name='cloud_aws_api'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_cloud_aws_new {
  local marker_name='cloud_aws_new'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_cloud_aws_cloudformation {
  local marker_name='cloud_aws_cloudformation'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_cloud_aws_terraform {
  local marker_name='cloud_aws_terraform'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_cloud_azure {
  local marker_name='cloud_azure'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_cloud_gcp {
  local marker_name='cloud_gcp'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_cloud_kubernetes {
  local marker_name='cloud_kubernetes'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_db_mssql {
  local marker_name='db_mssql'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_db_mysql {
  local marker_name='db_mysql'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_db_postgres {
  local marker_name='db_postgres'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_format {
  local marker_name='format'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_helper {
  local marker_name='helper'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_iot {
  local marker_name='iot'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_core {
  local marker_name='lang_core'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_csharp {
  local marker_name='lang_csharp'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_docker {
  local marker_name='lang_docker'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_dotnetconfig {
  local marker_name='lang_dotnetconfig'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_html {
  local marker_name='lang_html'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_java {
  local marker_name='lang_java'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_javascript {
  local marker_name='lang_javascript'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_php {
  local marker_name='lang_php'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_python {
  local marker_name='lang_python'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_rpgle {
  local marker_name='lang_rpgle'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_lang_times {
  local marker_name='lang_times'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_ot {
  local marker_name='ot'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_dns {
  local marker_name='proto_dns'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_ftp {
  local marker_name='proto_ftp'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_git {
  local marker_name='proto_git'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_graphql {
  local marker_name='proto_graphql'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_http {
  local marker_name='proto_http'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_ldap {
  local marker_name='proto_ldap'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_rest {
  local marker_name='proto_rest'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_smb {
  local marker_name='proto_smb'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_smtp {
  local marker_name='proto_smtp'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_ssh {
  local marker_name='proto_ssh'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_ssl {
  local marker_name='proto_ssl'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_proto_tcp {
  local marker_name='proto_tcp'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_sca {
  local marker_name='sca'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_syst {
  local marker_name='syst'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_api_utils {
  local marker_name='utils'

  trap "helper_asserts_mocks_ctl shutdown ${marker_name}" 'EXIT'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}" \
  &&  popd \
  ||  return 1
}

function job_asserts_test_output {
  export FA_NOTRACK='true'
  export FA_STRICT='false'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  asserts \
        --kiss \
        --multiprocessing \
        --show-method-stats \
        --cloudformation \
        test \
  &&  popd \
  ||  return 1
}

function job_asserts_build {
      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  helper_build_asserts \
  &&  cp -a asserts-release "${STARTDIR}/asserts" \
  &&  popd \
  || return 1
}

function job_asserts_release_pypi {
  local release_folder='asserts-release'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_with_production_secrets \
  &&  helper_build_asserts \
  &&  twine check "${release_folder}/"* \
  &&  twine upload "${release_folder}/"* \
  &&  popd \
  ||  return 1
}

function job_asserts_release_docker_hub {
  function build {
    local image_name="${1}"
    local target_name="${2}"
    local file="${3}"

        docker build  \
          --tag "${image_name}" \
          --target "${target_name}" \
          -f "${file}" \
          . \
    &&  docker push "${image_name}"
  }

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  helper_with_production_secrets \
  &&  docker login "${DOCKER_HUB_URL}" \
        --username "${DOCKER_HUB_USER}" \
        --password-stdin \
        <<< "${DOCKER_HUB_PASS}" \
  &&  build \
        'fluidattacks/asserts:debian-light' \
        'light' \
        'debian.Dockerfile' \
  &&  build \
        'fluidattacks/asserts:debian-full' \
        'full' \
        'debian.Dockerfile' \
  &&  build \
        'fluidattacks/asserts:debian' \
        'full' \
        'debian.Dockerfile' \
  &&  build \
        'fluidattacks/asserts' \
        'full' \
        'debian.Dockerfile' \
  &&  popd \
  ||  return 1
}

function job_asserts_documentation {
  local bucket_path='s3://web.fluidattacks.com/resources/doc/asserts/'

      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  env_prepare_python_packages \
  &&  helper_asserts_aws_login prod \
  &&  helper_pages_execute_example_exploits \
  &&  helper_pages_generate_credits \
  &&  helper_pages_generate_doc \
  &&  aws s3 sync output/ "${bucket_path}" --delete \
  &&  popd \
  ||  return 1
}
