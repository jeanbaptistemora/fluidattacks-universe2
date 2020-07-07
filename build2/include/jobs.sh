# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcEnv}"

function job_build_nix_caches {
  local provisioners
  local dockerfile
  local context='.'
  local dockerfile='build/Dockerfile'

      helper_use_pristine_workdir \
  &&  provisioners=(./build/provisioners/*) \
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

function job_test_autoscaling_ci {
      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        services/autoscaling-ci/terraform \
  &&  helper_terraform_lint \
        services/autoscaling-ci/terraform
}

function job_apply_autoscaling_ci {
      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        services/autoscaling-ci/terraform
}
