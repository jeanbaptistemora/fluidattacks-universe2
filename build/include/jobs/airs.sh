# shellcheck shell=bash

function job_airs_test_lint_code {
      helper_common_use_pristine_workdir \
  &&  pushd airs \
  &&  env_prepare_python_packages \
  &&  helper_airs_list_touched_files | xargs pre-commit run -v --files \
  &&  npm install --prefix theme/2020/ \
  &&  echo '[INFO] Testing Pelican website'\
  &&  npm run --prefix theme/2020/ lint \
  &&  popd \
  ||  return 1
}

function job_airs_test_generic {
  local all_content_files
  local touched_adoc_files
  local max_columns='81'
  local min_words='1'
  local max_words='4500'
  local max_lix='65'

      pushd airs \
  &&  helper_airs_set_lc_all \
  &&  all_content_files="$(find content/ -type f)" \
  &&  touched_adoc_files="$(helper_airs_list_touched_files | grep '.adoc')" || true \
  &&  echo '[INFO] Testing forbidden extensions' \
  &&  helper_airs_generic_forbidden_extensions \
  &&  echo '[INFO] Testing compliant file names' \
  &&  for path in ${all_content_files}
      do
            helper_airs_generic_file_name "${path}" \
        ||  return 1
      done \
  && echo '[INFO] Testing touched adoc files' \
  &&  for path in ${touched_adoc_files}
      do
            helper_airs_generic_adoc_keywords_uppercase "${path}" \
        &&  helper_airs_generic_adoc_fluid_attacks_name "${path}" \
        &&  helper_airs_generic_adoc_spelling "${path}" \
        &&  helper_airs_generic_adoc_others "${path}" \
        &&  helper_airs_adoc_tag_exists "${path}" ':description:' \
        &&  helper_airs_adoc_max_columns "${path}" "${max_columns}" \
        &&  helper_airs_word_count "${path}" "${min_words}" "${max_words}" \
        &&  helper_airs_test_lix "${path}" "${max_lix}" \
        ||  return 1
      done \
  &&  popd \
  ||  return 1
}

function job_airs_test_blog {
  local all_blog_adoc_files
  local touched_blog_adoc_files
  local min_words='800'
  local max_words='1200'
  local max_lix='50'

      pushd airs \
  &&  helper_airs_set_lc_all \
  &&  all_blog_adoc_files="$(find content/blog/ -type f -name '*.adoc')" \
  &&  touched_blog_adoc_files="$(helper_airs_list_touched_files | grep 'content/blog/' | grep '.adoc')" || true \
  &&  echo '[INFO] Testing adoc files' \
  &&  for path in ${all_blog_adoc_files}
      do
            helper_airs_blog_adoc_category "${path}" \
        &&  helper_airs_blog_adoc_tags "${path}" \
        &&  helper_airs_adoc_tag_exists "${path}" ':subtitle:' \
        &&  helper_airs_adoc_tag_exists "${path}" ':alt:' \
        ||  return 1
      done \
  &&  for path in ${touched_blog_adoc_files}
      do
            helper_airs_blog_adoc_others "${path}" \
        &&  helper_airs_adoc_tag_exists "${path}" ':source:' \
        &&  helper_airs_word_count "${path}" "${min_words}" "${max_words}" \
        &&  helper_airs_test_lix "${path}" "${max_lix}" \
        ||  return 1
      done \
  &&  popd \
  ||  return 1
}

function job_airs_test_defends {
  local touched_defends_adoc_files
  local min_words='400'
  local max_words='800'
  local max_lix='60'

      pushd airs \
  &&  helper_airs_set_lc_all \
  &&  touched_defends_adoc_files="$(helper_airs_list_touched_files | grep 'content/pages/products/defends/' | grep '.adoc')" || true \
  &&  echo '[INFO] Testing defends files' \
  &&  for path in ${touched_defends_adoc_files}
      do
            helper_airs_word_count "${path}" "${min_words}" "${max_words}" \
        &&  helper_airs_test_lix "${path}" "${max_lix}" \
        ||  return 1
      done \
  &&  popd \
  ||  return 1
}

function job_airs_test_lint_styles {
  local err_count

      pushd airs/theme/2020 \
  &&  npm install \
  &&  echo "[INFO] Running Stylelint to lint SCSS files" \
  &&  if npm run lint:stylelint
      then
        echo '[INFO] All styles are ok!'
      else
            err_count="$(npx stylelint '**/*.scss' | wc -l || true)" \
        &&  echo "[ERROR] ${err_count} errors found in styles!" \
        &&  return 1
      fi \
  &&  popd \
  || return 1
}

function job_airs_deploy_local {
      helper_common_use_pristine_workdir \
  &&  pushd airs \
  &&  npm cache clean --force \
  &&  helper_airs_set_lc_all \
  &&  helper_airs_compile 'http://localhost:8000' \
  &&  popd \
  &&  airs airs/output dev \
  ||  return 1
}

function job_airs_deploy_ephemeral {
      helper_common_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_set_lc_all \
  &&  helper_airs_aws_login development \
  &&  helper_airs_compile "https://web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}" \
  &&  popd \
  &&  airs airs/output eph \
  ||  return 1
}

function job_airs_deploy_production {
      helper_common_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_set_lc_all \
  &&  helper_airs_aws_login production \
  &&  helper_airs_compile 'https://fluidattacks.com' \
  &&  popd \
  &&  airs airs/output prod \
  ||  return 1
}
