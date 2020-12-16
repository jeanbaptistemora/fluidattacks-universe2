# shellcheck shell=bash

function job_integrates_lint_back {
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  mypy --strict --ignore-missing-imports analytics/ \
  &&  mypy --ignore-missing-imports --follow-imports=skip \
        backend_new/packages/integrates-back \
  &&  mypy --strict --ignore-missing-imports backend_new/migrations/ \
  &&  mypy --strict --ignore-missing-imports backend_new \
  &&  prospector -F -s veryhigh analytics/ \
  &&  prospector -F -s veryhigh -u django -i node_modules backend_new \
  &&  prospector -F -s veryhigh -u django -i node_modules backend_new/packages/integrates-back \
  &&  prospector -F -s veryhigh -u django -i node_modules fluidintegrates \
  &&  prospector -F -s veryhigh lambda \
  &&  prospector -F -s veryhigh -u django -i node_modules deploy/permissions-matrix \
  &&  npx graphql-schema-linter \
        --except 'enum-values-have-descriptions,fields-are-camel-cased,fields-have-descriptions,input-object-values-are-camel-cased,relay-page-info-spec,types-have-descriptions,arguments-have-descriptions' \
        backend_new/packages/integrates-back/backend/api/schema/**/*.graphql \
        backend_new/packages/integrates-back/backend/api/schema/types/**/*.graphql \
  &&  popd \
  || return 1
}

function job_integrates_lint_e2e {
  local modules=(
    src/
    src/tests/
  )

      pushd integrates/test_e2e \
    &&  env_prepare_python_packages \
    &&  mypy --config-file settings.cfg "${modules[@]}" \
    &&  prospector --profile profile.yaml . \
  &&  popd \
  ||  return 1
}

function job_integrates_lint_front {
        pushd "${STARTDIR}/integrates/front" \
    &&  npm install \
    &&  npm audit \
    &&  npm run lint:tslint \
    &&  npm run lint:eslint \
    &&  popd \
    ||  return 1
}

function job_integrates_lint_styles {
  local err_count
        pushd "${STARTDIR}/integrates/front" \
      &&  npm install \
      &&  echo "[INFO] Running Stylelint to lint CSS files" \
      &&  if npm run lint:stylelint
          then
            echo '[INFO] All styles are ok!'
          else
                err_count="$(npx stylelint '**/*.css' | wc -l || true)" \
            &&  echo "[ERROR] ${err_count} errors found in styles!" \
            &&  return 1
          fi \
    && popd \
    || return 1
}

function job_integrates_lint_graphics {
      env_prepare_node_modules \
  &&  pushd "${STARTDIR}/integrates/backend_new/app/templates/static/graphics" \
        &&  eslint --config .eslintrc --fix . \
  &&  popd \
  ||  return 1
}

function job_integrates_lint_mobile {
      pushd "${STARTDIR}/integrates/mobile" \
    &&  npm install \
    &&  npm run lint \
  &&  popd \
  ||  return 1
}

function job_integrates_lint_secrets {
  local files_to_verify=(
    secrets-development.yaml
    secrets-production.yaml
  )
      pushd "${STARTDIR}/integrates" \
  &&  env_prepare_python_packages \
  &&  echo "[INFO] Veryfing that secrets is sorted" \
  &&  for sf in "${files_to_verify[@]}"
      do
            echo "  [INFO] Veryfing that ${sf} is sorted" \
        &&  head -n -13 "${sf}" > "temp-${sf}" \
        &&  yamllint --no-warnings -d "{extends: relaxed, rules: {key-ordering: {level: error}}}" "temp-${sf}" \
        &&  rm "temp-${sf}"
      done \
  &&  popd \
  || return 1
}
