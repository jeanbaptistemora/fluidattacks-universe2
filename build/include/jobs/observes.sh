# shellcheck shell=bash

function job_observes_gitlab {
  export PATH="${PATH}:${EtlGitlab}/bin"
      helper_common_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_gitlab \
  ||  return 1
}

function job_observes_gitlab_on_aws {
  local vcpus='1'
  local memory='3600'
  local attempts='10'
  local timeout='14400'
  local jobname="observes_gitlab"
  local jobqueue='spot_later'

      helper_observes_aws_login prod \
  &&  helper_common_run_on_aws \
        "${vcpus}" \
        "${memory}" \
        "${attempts}" \
        "${timeout}" \
        "${jobname}" \
        "${jobqueue}" \
        'observes_gitlab'
}

function job_observes_zoho {
      helper_common_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_zoho \
  ||  return 1
}

function job_observes_zoho_crm_prepare {
  export PATH="${PATH}:${StreamerZoho}/bin"
      helper_common_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_zoho_crm_prepare \
  ||  return 1
}

function job_observes_zoho_crm {
  export PATH="${PATH}:${StreamerZoho}/bin"

      helper_common_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_zoho_crm \
  ||  return 1
}

function job_observes_timedoctor_refresh_token {
      helper_common_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_refresh_token \
  ||  return 1
}

function job_observes_timedoctor_manually_create_token {
      helper_common_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_observes_timedoctor_manually_create_token \
  ||  return 1
}
