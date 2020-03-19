# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcEnv}"

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

function job_lint_pre_commit {
      env_prepare_python_packages \
  &&  helper_list_touched_files | xargs pre-commit run -v --files
}

function job_test_images {
  local blog_covers
  local png_images
  local all_images

      blog_covers="$(find content/blog/ -type f -name cover.png)" \
  &&  png_images="$(find content/ -type f -name '*.png')" \
  &&  all_images="$(find content/ -name '*' -exec file --mime-type {} \; | grep -oP '.*(?=: image/)')" \
  &&  echo '[INFO] Testing all images' \
  &&  for image in ${all_images}
      do
            helper_image_valid "${image}" || return 1
      done \
  &&  echo '[INFO] Testing blog covers' \
  &&  for cover in ${blog_covers}
      do
            helper_blog_cover_has_proper_dimensions "${cover}" || return 1
      done \
  &&  echo '[INFO] Testing PNG images' \
  &&  for image in ${png_images}
      do
            helper_image_optimized "${image}" \
        &&  helper_image_size "${image}" || return 1
      done
}
