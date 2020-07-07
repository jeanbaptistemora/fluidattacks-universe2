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

function job_test_infra_autoscaling_ci {
  local target='services/autoscaling-ci/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_autoscaling_ci {
  local target='services/autoscaling-ci/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_infra_analytics {
  local target='services/analytics/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_analytics {
  local target='services/analytics/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_infra_aws_sso {
  local target='services/aws-sso/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_aws_sso {
  local target='services/aws-sso/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_infra_fluid_vpc {
  local target='services/fluid-vpc/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_fluid_vpc {
  local target='services/fluid-vpc/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_infra_secret_management {
  local target='secret-management/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_secret_management {
  local target='secret-management/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_commit_msg {
      helper_use_pristine_workdir \
  &&  env_prepare_node_modules \
  &&  helper_test_commit_msg_commitlint
}
