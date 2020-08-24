# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcIncludeHelpersServes}"
source "${srcIncludeHelpersObserves}"

function job_observes_formstack {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_formstack \
  ||  return 1
}

function job_observes_dynamodb {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_dynamodb \
  ||  return 1
}

function job_observes_services_toe {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_services_toe \
  ||  return 1
}

function job_observes_infrastructure {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_infrastructure \
  ||  return 1
}

function job_observes_intercom {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_intercom \
  ||  return 1
}

function job_observes_mandrill {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_mandrill \
  ||  return 1
}

function job_observes_gitlab {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_gitlab \
  ||  return 1
}

function job_observes_timedoctor {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor \
  ||  return 1
}

function job_observes_zoho {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_zoho \
  ||  return 1
}

function job_observes_git_process {
  # If you move me take into account the artifacts in the .gitlab-ci.yaml

      env_prepare_python_packages \
  &&  helper_observes_git_process \
  ||  return 1
}

function job_observes_git_upload {
      env_prepare_python_packages \
  &&  helper_observes_git_upload \
  ||  return 1
}

function job_observes_timedoctor_refresh_token {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_refresh_token \
  ||  return 1
}

function job_observes_timedoctor_backup {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_backup \
  ||  return 1
}

function job_observes_timedoctor_manually_create_token {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_manually_create_token \
  ||  return 1
}

function job_observes_services_repositories_cache {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_services_repositories_cache \
  ||  return 1
}

function job_serves_test_infra_analytics {
  local target='services/analytics/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_serves_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_infra_analytics {
  local target='services/analytics/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_serves_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}
