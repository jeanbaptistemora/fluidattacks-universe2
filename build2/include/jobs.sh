# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcEnv}"

function job_build_nix_caches {
  local context='.'
  local dockerfile='build/Dockerfile'
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
