# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcIncludeHelpersServes}"
source "${srcIncludeHelpersObserves}"

function job_analytics_formstack {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_formstack \
  &&  popd \
  ||  return 1
}

function job_analytics_dynamodb {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_dynamodb \
  &&  popd \
  ||  return 1
}

function job_analytics_services_toe {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_services_toe \
  &&  popd \
  ||  return 1
}

function job_analytics_infrastructure {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_infrastructure \
  &&  popd \
  ||  return 1
}

function job_analytics_intercom {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_intercom \
  &&  popd \
  ||  return 1
}

function job_analytics_mandrill {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_mandrill \
  &&  popd \
  ||  return 1
}

function job_analytics_gitlab {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_gitlab \
  &&  popd \
  ||  return 1
}

function job_analytics_timedoctor {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor \
  &&  popd \
  ||  return 1
}

function job_analytics_zoho {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_zoho \
  &&  popd \
  ||  return 1
}

function job_analytics_git_process {
  # If you move me take into account the artifacts in the .gitlab-ci.yaml

      pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_git_process \
  &&  popd \
  ||  return 1
}

function job_analytics_git_upload {
      pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_git_upload \
  &&  popd \
  ||  return 1
}

function job_analytics_timedoctor_refresh_token {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_refresh_token \
  &&  popd \
  ||  return 1
}

function job_analytics_timedoctor_backup {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_backup \
  &&  popd \
  ||  return 1
}

function job_analytics_timedoctor_manually_create_token {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_manually_create_token \
  &&  popd \
  ||  return 1
}

function job_analytics_services_repositories_cache {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  env_prepare_python_packages \
  &&  helper_observes_services_repositories_cache \
  &&  popd \
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
