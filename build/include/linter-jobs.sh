# shellcheck shell=bash

function job_lint_back {
      env_prepare_python_packages \
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
        django-apps/integrates-back-async/backend/api/schemas/*
}

function job_lint_build_system {
  # SC1090: Can't follow non-constant source. Use a directive to specify location.
  # SC2016: Expressions don't expand in single quotes, use double quotes for that.
  # SC2153: Possible misspelling: TEMP_FILE2 may not be assigned, but TEMP_FILE1 is.
  # SC2154: var is referenced but not assigned.

      nix-linter --recursive . \
  && echo '[OK] Nix code is compliant'
      shellcheck --external-sources build.sh \
  && find 'build' -name '*.sh' -exec \
      shellcheck --external-sources --exclude=SC1090,SC2016,SC2153,SC2154 {} + \
  && echo '[OK] Shell code is compliant'
}

function job_lint_front {
      pushd front \
    &&  npm install \
    &&  npm audit \
    &&  npm run lint:tslint \
    &&  npm run lint:eslint \
  &&  popd \
  ||  return 1
}

function job_lint_graphics {
      env_prepare_node_modules \
  &&  pushd app/static/graphics \
        &&  eslint --config .eslintrc --fix . \
  &&  popd \
  ||  return 1
}

function job_lint_mobile {
      pushd mobile \
    &&  npm install \
    &&  npm run lint \
  &&  popd \
  ||  return 1
}

function job_lint_secrets {
  local files_to_verify=(
    secrets-development.yaml
    secrets-production.yaml
  )
      env_prepare_python_packages \
  &&  echo "[INFO] Veryfing that secrets is sorted" \
  &&  for sf in "${files_to_verify[@]}"
      do
            echo "  [INFO] Veryfing that ${sf} is sorted" \
        &&  head -n -13 "${sf}" > "temp-${sf}" \
        &&  yamllint --no-warnings -d "{extends: relaxed, rules: {key-ordering: {level: error}}}" "temp-${sf}" \
        &&  rm "temp-${sf}"
      done
}

function job_lint_commit_msg {
  local commit_diff
  local commit_hashes
  local parser_url='https://static-objects.gitlab.net/fluidattacks/public/raw/master/commitlint-configs/others/parser-preset.js'
  local rules_url='https://static-objects.gitlab.net/fluidattacks/public/raw/master/commitlint-configs/others/commitlint.config.js'

      helper_use_pristine_workdir \
  &&  curl -LOJ "${parser_url}" \
  &&  curl -LOJ "${rules_url}" \
  &&  npm install @commitlint/{config-conventional,cli} \
  &&  git fetch --prune > /dev/null \
  &&  if [ "${IS_LOCAL_BUILD}" = "${TRUE}" ]
      then
            commit_diff="origin/master..${CI_COMMIT_REF_NAME}"
      else
            commit_diff="origin/master..origin/${CI_COMMIT_REF_NAME}"
      fi \
  &&  commit_hashes="$(git log --pretty=%h "${commit_diff}")" \
  &&  for commit_hash in ${commit_hashes}
      do
            git log -1 --pretty=%B "${commit_hash}" | npx commitlint \
        ||  return 1
      done
}
