# shellcheck shell=bash

function job_integrates_lint_back {
      pushd integrates/ \
  &&  env_prepare_python_packages \
  &&  mypy --strict --ignore-missing-imports analytics/ \
  &&  mypy --ignore-missing-imports --follow-imports=skip \
        django-apps/integrates-back-async \
  &&  mypy --strict --ignore-missing-imports app/migrations/ \
  &&  prospector -F -s veryhigh analytics/ \
  &&  prospector -F -s high -u django -i node_modules app \
  &&  prospector -F -s veryhigh -u django -i node_modules django-apps/integrates-back-async \
  &&  prospector -F -s veryhigh -u django -i node_modules fluidintegrates \
  &&  prospector -F -s veryhigh lambda \
  &&  prospector -F -s veryhigh -u django -i node_modules deploy/permissions-matrix \
  &&  npx graphql-schema-linter \
        --except 'enum-values-all-caps,enum-values-have-descriptions,fields-are-camel-cased,fields-have-descriptions,input-object-values-are-camel-cased,relay-page-info-spec,types-have-descriptions,type-fields-sorted-alphabetically,arguments-have-descriptions,type-fields-sorted-alphabetically' \
        django-apps/integrates-back-async/backend/api/schemas/* \
  &&  popd \
  || return 1
}

function job_integrates_lint_front {
        pushd integrates/front/ \
    &&  npm install \
    &&  npm audit \
    &&  npm run lint:tslint \
    &&  npm run lint:eslint \
    &&  popd \
    ||  return 1
}

function job_integrates_lint_graphics {
      env_prepare_node_modules \
  &&  pushd integrates/app/static/graphics \
        &&  eslint --config .eslintrc --fix . \
  &&  popd \
  ||  return 1
}

function job_integrates_lint_mobile {
      pushd integrates/mobile \
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
      pushd integrates/ \
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
