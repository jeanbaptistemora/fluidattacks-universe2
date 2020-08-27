# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"
source "${srcIncludeHelpersAsserts}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"

function job_asserts_build_asserts {
      helper_use_pristine_workdir \
  &&  pushd asserts \
  &&  helper_build_asserts \
  &&  cp -a asserts-release "${STARTDIR}" \
  &&  popd \
  || return 1
}

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
  &&  helper_config_precommit \
  &&  helper_common_list_touched_files | xargs pre-commit run -v --files \
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

function job_asserts_test_infra_secret_management {
  local dir='deploy/secret-management/terraform'

      helper_use_pristine_workdir \
  &&  helper_asserts_aws_login dev \
  &&  helper_terraform_test "${dir}"
}

function job_asserts_deploy_infra_secret_management {
  local dir='deploy/secret-management/terraform'

      helper_use_pristine_workdir \
  &&  helper_asserts_aws_login prod \
  &&  helper_terraform_apply "${dir}"
}

function job_asserts_test_api_cloud_aws_api {
  local marker_name='cloud_aws_api'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_cloud_aws_new {
  local marker_name='cloud_aws_new'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_cloud_aws_cloudformation {
  local marker_name='cloud_aws_cloudformation'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_cloud_aws_terraform {
  local marker_name='cloud_aws_terraform'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_cloud_azure {
  local marker_name='cloud_azure'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_cloud_gcp {
  local marker_name='cloud_gcp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_cloud_kubernetes {
  local marker_name='cloud_kubernetes'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_db_mssql {
  local marker_name='db_mssql'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_db_mysql {
  local marker_name='db_mysql'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_db_postgres {
  local marker_name='db_postgres'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_format {
  local marker_name='format'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_helper {
  local marker_name='helper'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_iot {
  local marker_name='iot'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_core {
  local marker_name='lang_core'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_csharp {
  local marker_name='lang_csharp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_docker {
  local marker_name='lang_docker'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_dotnetconfig {
  local marker_name='lang_dotnetconfig'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_html {
  local marker_name='lang_html'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_java {
  local marker_name='lang_java'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_javascript {
  local marker_name='lang_javascript'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_php {
  local marker_name='lang_php'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_python {
  local marker_name='lang_python'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_rpgle {
  local marker_name='lang_rpgle'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_lang_times {
  local marker_name='lang_times'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_ot {
  local marker_name='ot'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_dns {
  local marker_name='proto_dns'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_ftp {
  local marker_name='proto_ftp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_git {
  local marker_name='proto_git'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_graphql {
  local marker_name='proto_graphql'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_http {
  local marker_name='proto_http'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_ldap {
  local marker_name='proto_ldap'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_rest {
  local marker_name='proto_rest'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_smb {
  local marker_name='proto_smb'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_smtp {
  local marker_name='proto_smtp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_ssh {
  local marker_name='proto_ssh'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_ssl {
  local marker_name='proto_ssl'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_proto_tcp {
  local marker_name='proto_tcp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_sca {
  local marker_name='sca'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_syst {
  local marker_name='syst'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_api_utils {
  local marker_name='utils'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_asserts_test_output_asserts {
  export FA_NOTRACK='true'
  export FA_STRICT='false'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  asserts \
        --kiss \
        --multiprocessing \
        --show-method-stats \
        --cloudformation \
        test
}

function job_asserts_release_to_pypi {
  local release_folder='asserts-release'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_with_production_secrets \
  &&  helper_build_asserts \
  &&  twine check "${release_folder}/"* \
  &&  twine upload "${release_folder}/"*
}

function job_asserts_release_to_docker_hub {
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
        'debian.Dockerfile'
}

function job_asserts_pages {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_pages_execute_example_exploits \
  &&  helper_pages_generate_credits \
  &&  helper_pages_generate_doc \
  &&  mv public/ "${STARTDIR}"
}
