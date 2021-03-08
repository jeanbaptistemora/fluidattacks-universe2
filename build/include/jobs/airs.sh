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
  &&  airs dev \
  ||  return 1
}

function job_airs_deploy_ephemeral {
      helper_common_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_set_lc_all \
  &&  helper_airs_aws_login development \
  &&  helper_airs_compile "https://web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}" \
  &&  popd \
  &&  airs eph \
  ||  return 1
}

function job_airs_deploy_production {
      helper_common_use_pristine_workdir \
  &&  pushd airs \
  &&  helper_airs_set_lc_all \
  &&  helper_airs_aws_login production \
  &&  helper_airs_compile 'https://fluidattacks.com' \
  &&  popd \
  &&  airs prod \
  ||  return 1
}
