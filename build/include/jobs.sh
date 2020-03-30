# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcIncludeHelpersBlog}"
source "${srcIncludeHelpersDeploy}"
source "${srcIncludeHelpersGeneric}"
source "${srcIncludeHelpersImage}"
source "${srcEnv}"

function job_build_nix_caches {
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

function job_test_pre_commit {
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
  local touched_adoc_files
  local max_columns='81'
  local min_words='10'
  local max_words='1600'
  local max_lix='65'

      all_content_files="$(find content/ -type f)" \
  &&  all_adoc_files="$(find content/ -type f -name '*.adoc')" \
  &&  touched_adoc_files="$(helper_list_touched_files | grep '.adoc')" || true \
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
        &&  helper_generic_adoc_others "${path}" \
        &&  helper_adoc_tag_exists "${path}" ':description:' \
        &&  helper_adoc_max_columns "${path}" "${max_columns}" \
        ||  return 1
      done \
  &&  for path in ${touched_adoc_files}
      do
            helper_word_count "${path}" "${min_words}" "${max_words}" \
        &&  helper_test_lix "${path}" "${max_lix}" \
        ||  return 1
      done
}

function job_test_blog {
  local all_blog_adoc_files
  local touched_blog_adoc_files
  local min_words='800'
  local max_words='1600'
  local max_lix='50'

      all_blog_adoc_files="$(find content/blog/ -type f -name '*.adoc')" \
  &&  touched_blog_adoc_files="$(helper_list_touched_files | grep 'content/blog/' | grep '.adoc')" || true \
  &&  echo '[INFO] Testing adoc files' \
  &&  for path in ${all_blog_adoc_files}
      do
            helper_blog_adoc_category "${path}" \
        &&  helper_blog_adoc_tags "${path}" \
        &&  helper_adoc_tag_exists "${path}" ':subtitle:' \
        &&  helper_adoc_tag_exists "${path}" ':alt:' \
        ||  return 1
      done \
  &&  for path in ${touched_blog_adoc_files}
      do
            helper_blog_adoc_others "${path}" \
        &&  helper_adoc_tag_exists "${path}" ':source:' \
        &&  helper_word_count "${path}" "${min_words}" "${max_words}" \
        &&  helper_test_lix "${path}" "${max_lix}" \
        ||  return 1
      done
}

function job_test_defends {
  local touched_defends_adoc_files
  local min_words='400'
  local max_words='800'
  local max_lix='60'

      touched_defends_adoc_files="$(helper_list_touched_files | grep 'content/pages/defends/' | grep '.adoc')" || true \
  &&  echo '[INFO] Testing defends files' \
  &&  for path in ${touched_defends_adoc_files}
      do
            helper_word_count "${path}" "${min_words}" "${max_words}" \
        &&  helper_test_lix "${path}" "${max_lix}" \
        ||  return 1
      done
}

function job_deploy_ephemeral_local {
  local base_folder='deploy/builder'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  npm install --prefix "${base_folder}" \
  &&  PATH="${PATH}:$(pwd)/${base_folder}/node_modules/.bin/" \
  &&  sed -i "s#\$flagsImagePath:.*#\$flagsImagePath:\ \"../../images/\";#" "${base_folder}/node_modules/intl-tel-input/src/css/intlTelInput.scss" \
  && helper_deploy_install_plugins \
  &&  cp -a js theme/2014/static/ \
  &&  PATH="${PATH}:${base_folder}/node_modules/uglify-js/bin/" \
  &&  cp -a "${base_folder}/node_modules" theme/2014/ \
  &&  cp -a "${base_folder}/node_modules" . \
  &&  cp -a "${base_folder}/node_modules" theme/2014/static/ \
  &&  sed -i "s|https://fluidattacks.com|http://localhost:8000|g" pelicanconf.py \
  &&  sed -i "s|/app/pelican-plugins|pelican-plugins|g" pelicanconf.py \
  &&  sed -i "s|/app/js/|js/|g" theme/2014/templates/base.html \
  &&  sed -i "s|/app/deploy/builder/node_modules/|node_modules/|g" theme/2014/templates/base.html \
  &&  sed -i "s|/app/deploy/builder/node_modules/|node_modules/|g" theme/2014/templates/contact.html \
  &&  npm run --prefix "${base_folder}" build \
  &&  cp -a "${STARTDIR}/cache" . || true \
  &&  ./build-site.sh \
  &&  cp -a cache/ "${STARTDIR}" || true \
  &&  cp -a "${base_folder}/node_modules" new/theme/2014/ \
  &&  cp -a "${base_folder}/node_modules" new/theme/2014/static/ \
  &&  cp -a "${base_folder}/node_modules" new/ \
  &&  sed -i "s|https://fluidattacks.com|http://localhost:8000|g" new/pelicanconf.py \
  &&  sed -i "s|/app/pelican-plugins|../pelican-plugins|g" new/pelicanconf.py \
  &&  pushd new/ || return 1 \
  &&  npm run --prefix "../${base_folder}" build-new \
  &&  cp -a "${STARTDIR}/new/cache" . || true \
  &&  ./build-site.sh \
  &&  cp -a cache/ "${STARTDIR}/new" || true \
  &&  popd || return 1 \
  &&  cp -a new/output/newweb output/ \
  &&  python3 -m http.server --directory output
}
