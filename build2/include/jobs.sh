# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcEnv}"

function job_build_nix_caches {
  local context='.'
  local dockerfile='build2/Dockerfile'
  local provisioners

      helper_use_pristine_workdir \
  &&  provisioners=(./build2/provisioners/*) \
  &&  helper_build_nix_caches_parallel \
  &&  for (( i="${lower_limit}";i<="${upper_limit}";i++ ))
      do
            provisioner=$(basename "${provisioners[${i}]}") \
        &&  provisioner="${provisioner%.*}" \
        &&  helper_docker_build_and_push \
              "${CI_REGISTRY_IMAGE}/nix:${provisioner}" \
              "${context}" \
              "${dockerfile}" \
              'PROVISIONER' "${provisioner}" \
        ||  return 1
      done
}

function job_test_asserts_api_cloud_aws_cloudformation {
  local marker_name='cloud_aws_cloudformation'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_cloud_aws_terraform {
  local marker_name='cloud_aws_terraform'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_cloud_azure {
  local marker_name='cloud_azure'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_cloud_gcp {
  local marker_name='cloud_gcp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_cloud_kubernetes {
  local marker_name='cloud_kubernetes'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_db_mssql {
  local marker_name='db_mssql'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_db_mysql {
  local marker_name='db_mysql'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_db_postgres {
  local marker_name='db_postgres'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_format {
  local marker_name='format'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_helper {
  local marker_name='helper'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_iot {
  local marker_name='iot'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_core {
  local marker_name='lang_core'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_csharp {
  local marker_name='lang_csharp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_docker {
  local marker_name='lang_docker'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_dotnetconfig {
  local marker_name='lang_dotnetconfig'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_html {
  local marker_name='lang_html'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_java {
  local marker_name='lang_java'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_javascript {
  local marker_name='lang_javascript'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_php {
  local marker_name='lang_php'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}
