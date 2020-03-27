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
            helper_image_valid "${image}" \
        ||  return 1
      done \
  &&  echo '[INFO] Testing blog covers' \
  &&  for cover in ${blog_covers}
      do
            helper_image_blog_cover_dimensions "${cover}" \
        ||  return 1
      done \
  &&  echo '[INFO] Testing PNG images' \
  &&  for image in ${png_images}
      do
            helper_image_optimized "${image}" \
        &&  helper_image_size "${image}" \
        ||  return 1
      done
}

function job_test_generic {
  local all_content_files
  local all_adoc_files

      all_content_files="$(find content/ -type f)" \
  &&  all_adoc_files="$(find content/ -type f -name '*.adoc')" \
  &&  echo '[INFO] Testing forbidden extensions' \
  &&  helper_generic_forbidden_extensions \
  &&  echo '[INFO] Testing compliant file names' \
  &&  for path in ${all_content_files}
      do
            helper_generic_file_name "${path}" \
        ||  return 1
      done \
  && echo '[INFO] Testing adoc files' \
  &&  for path in ${all_adoc_files}
      do
            helper_generic_adoc_main_title "${path}" \
        &&  helper_generic_adoc_min_keywords "${path}" \
        &&  helper_generic_adoc_keywords_uppercase "${path}" \
        &&  helper_generic_adoc_fluid_attacks_name "${path}" \
        &&  helper_generic_adoc_spelling "${path}" \
        &&  helper_adoc_tag_exists "${path}" ':description:' \
        &&  helper_generic_adoc_others "${path}" \
        ||  return 1
      done
}

function job_test_blog {
  local all_blog_adoc_files
  local touched_blog_adoc_files
  local min_words='800'
  local max_words='1200'
  local allowed_columns='81'

      all_blog_adoc_files="$(find content/blog/ -type f -name '*.adoc')" \
  &&  touched_blog_adoc_files="$(helper_list_touched_files | grep 'content/blog/' | grep '.adoc')" || true \
  &&  echo '[INFO] Testing adoc files' \
  &&  for path in ${all_blog_adoc_files}
      do
            helper_blog_adoc_category "${path}" \
        &&  helper_blog_adoc_tags "${path}" \
        &&  helper_adoc_tag_exists "${path}" ':subtitle:' \
        &&  helper_adoc_tag_exists "${path}" ':alt:' \
        &&  helper_adoc_max_columns "${path}" "${allowed_columns}" \
        ||  return 1
      done \
  &&  for path in ${touched_blog_adoc_files}
      do
            helper_word_count "${path}" "${min_words}" "${max_words}" \
        &&  helper_adoc_tag_exists "${path}" ':source:' \
        &&  helper_blog_adoc_others "${path}" \
        ||  return 1
      done
}

function job_test_lix {
  local touched_adoc_files
  local touched_adoc_others
  local touched_adoc_rules
  local file_lix
  local others_lix='50'
  local rules_lix='65'

      touched_adoc_files="$(helper_list_touched_files | grep '.adoc')" || true \
  &&  touched_adoc_others="$(echo "${touched_adoc_files}" | grep -v 'content/pages/rules/')" || true \
  &&  touched_adoc_rules="$(echo "${touched_adoc_files}" | grep 'content/pages/rules/')" || true \
  &&  echo '[INFO] Testing Lix for touched adoc files' \
  &&  for path in ${touched_adoc_others}
      do
            file_lix="$(helper_get_lix "${path}")" \
        &&  if [ "${file_lix}" -le ${others_lix} ]
            then
                  continue
            else
                  echo "[ERROR] ${path} has Lix greater than ${others_lix}: ${file_lix}" \
              &&  return 1
            fi
      done \
  &&  for path in ${touched_adoc_rules}
      do
            file_lix="$(helper_get_lix "${path}")" \
        &&  if [ "${file_lix}" -le ${rules_lix} ]
            then
                  continue
            else
                  echo "[ERROR] ${path} has Lix greater than ${rules_lix}: ${file_lix}" \
              &&  return 1
            fi
      done
}
