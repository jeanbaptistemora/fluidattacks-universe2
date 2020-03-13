# shellcheck shell=bash

source "${srcIncludeHelpers}"

function job_deploy_container_nix_caches {
  local context='.'
  local dockerfile='build/Dockerfile'
  local provisioner
  local provisioner_path

      helper_use_pristine_workdir \
  &&  for provisioner_path in ./build/provisioners/*
      do
            provisioner=$(basename "${provisioner_path}") \
        &&  provisioner="${provisioner%.*}" \
        &&  if [ "${provisioner}" = 'deploy_container_nix_caches' ]
            then
                  echo '[INFO] Skipping deploy_container_nix_caches' \
              &&  continue
            fi \
        &&  echo "Building ${provisioner}" \
        &&  helper_docker_build_and_push \
              "${CI_REGISTRY_IMAGE}/nix:${provisioner}" \
              "${context}" \
              "${dockerfile}" \
              'PROVISIONER' "${provisioner}" \
        ||  return 1
      done
}

function job_infra_ephemeral_test {
  local dir='deploy/ephemeral/terraform'

      helper_set_dev_secrets \
  &&  helper_terraform_test "${dir}"
}

function job_infra_production_test {
  local dir='deploy/production/terraform'

      helper_set_dev_secrets \
  &&  helper_terraform_test "${dir}"
}

function job_infra_secret_management_test {
  local dir='deploy/secret-management/terraform'

      helper_set_dev_secrets \
  &&  helper_terraform_test "${dir}"
}

function job_infra_ephemeral_apply {
  local dir='deploy/ephemeral/terraform'

      helper_set_prod_secrets \
  &&  helper_terraform_apply "${dir}"
}

function job_infra_production_apply {
  local dir='deploy/production/terraform'

      helper_set_prod_secrets \
  &&  helper_terraform_apply "${dir}"
}

function job_infra_secret_management_apply {
  local dir='deploy/secret-management/terraform'

      helper_set_prod_secrets \
  &&  helper_terraform_apply "${dir}"
}
