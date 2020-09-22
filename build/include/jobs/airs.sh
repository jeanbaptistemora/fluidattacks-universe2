# shellcheck shell=bash

function job_airs_infra_ephemeral_test {
  local dir='deploy/ephemeral/terraform'

      helper_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_aws_login development \
  &&  helper_common_terraform_plan "${dir}" \
  &&  popd \
  ||  return 1
}

function job_airs_infra_production_test {
  local dir='deploy/production/terraform'

      helper_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_aws_login development \
  &&  helper_common_terraform_plan "${dir}" \
  &&  popd \
  ||  return 1
}

function job_airs_infra_secret_management_test {
  local dir='deploy/secret-management/terraform'

      helper_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_aws_login development \
  &&  helper_common_terraform_plan "${dir}" \
  &&  popd \
  ||  return 1
}

function job_airs_infra_ephemeral_apply {
  local dir='deploy/ephemeral/terraform'

      helper_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_aws_login production \
  &&  helper_common_terraform_apply "${dir}" \
  &&  popd \
  ||  return 1
}

function job_airs_infra_production_apply {
  local dir='deploy/production/terraform'

      helper_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_aws_login production \
  &&  helper_common_terraform_apply "${dir}" \
  &&  popd \
  ||  return 1
}

function job_airs_infra_secret_management_apply {
  local dir='deploy/secret-management/terraform'

      helper_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_aws_login production \
  &&  helper_common_terraform_apply "${dir}" \
  &&  popd \
  ||  return 1
}

function job_test_lint_code {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_list_touched_files | xargs pre-commit run -v --files \
  &&  npm install --prefix theme/2020/ \
  &&  npm run --prefix theme/2020/ lint
}

function job_test_images {
  local blog_covers
  local touched_png_images
  local all_images

      blog_covers="$(find content/blog/ -type f -name cover.png)" \
  &&  touched_png_images="$(helper_list_touched_files | grep '.png')" || true \
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
  &&  for image in ${touched_png_images}
      do
            helper_image_optimized "${image}" \
        &&  helper_image_size "${image}" \
        ||  return 1
      done
}

function job_test_generic {
  local all_content_files
  local touched_adoc_files
  local max_columns='81'
  local min_words='1'
  local max_words='4500'
  local max_lix='65'

      all_content_files="$(find content/ -type f)" \
  &&  touched_adoc_files="$(helper_list_touched_files | grep '.adoc')" || true \
  &&  echo '[INFO] Testing forbidden extensions' \
  &&  helper_generic_forbidden_extensions \
  &&  echo '[INFO] Testing compliant file names' \
  &&  for path in ${all_content_files}
      do
            helper_generic_file_name "${path}" \
        ||  return 1
      done \
  && echo '[INFO] Testing touched adoc files' \
  &&  for path in ${touched_adoc_files}
      do
            helper_generic_adoc_main_title "${path}" \
        &&  helper_generic_adoc_min_keywords "${path}" \
        &&  helper_generic_adoc_keywords_uppercase "${path}" \
        &&  helper_generic_adoc_fluid_attacks_name "${path}" \
        &&  helper_generic_adoc_spelling "${path}" \
        &&  helper_generic_adoc_others "${path}" \
        &&  helper_adoc_tag_exists "${path}" ':description:' \
        &&  helper_adoc_max_columns "${path}" "${max_columns}" \
        &&  helper_word_count "${path}" "${min_words}" "${max_words}" \
        &&  helper_test_lix "${path}" "${max_lix}" \
        ||  return 1
      done
}

function job_test_blog {
  local all_blog_adoc_files
  local touched_blog_adoc_files
  local min_words='800'
  local max_words='1450'
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

function job_deploy_local {
      helper_use_pristine_workdir \
  &&  helper_deploy_compile_web 'http://localhost:8000' \
  &&  python3 -m http.server --directory output
}

function job_deploy_ephemeral {
      helper_use_pristine_workdir \
  &&  helper_airs_aws_login development \
  &&  helper_deploy_compile_web "https://web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}" \
  &&  helper_deploy_sync_s3 'output/' "web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}"
}

function job_deploy_stop_ephemeral {
      helper_airs_aws_login development \
  &&  aws s3 rm "s3://web.eph.fluidattacks.com/$CI_COMMIT_REF_NAME" --recursive
}

function job_deploy_production {
      helper_use_pristine_workdir \
  &&  helper_airs_aws_login production \
  &&  helper_deploy_compile_web 'https://fluidattacks.com' \
  &&  helper_deploy_sync_s3 'output/' 'web.fluidattacks.com'
}
