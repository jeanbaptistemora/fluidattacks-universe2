# shellcheck shell=bash

function main {
  export BATCH_BIN
  if [[ $# -eq 0 ]] || [[ $# -gt 1 ]]; then
    echo '$ Error, add not_changes_db or changes_db to the command'
    exit 1
  else
    local test_group="${1}"
    export COVERAGE_FILE=.coverage.unit_"${test_group}"
    echo "$ Executing uni test with $test_group"
  fi
  local pytest_args=(
    --cov 'back'
    --cov-config 'back/test/unit/settings.cfg'
    --cov-report 'term'
    --cov-report 'html:build/coverage/html'
    --cov-report 'xml:coverage.xml'
    --cov-report 'annotate:build/coverage/annotate'
    --disable-warnings
    --no-cov-on-fail
    --verbose
  )

  source __argIntegratesBackEnv__/template dev \
    && if [ "$test_group" = "not_changes_db" ]; then
      DAEMON=true integrates-db \
        && export AWS_S3_PATH_PREFIX="${CI_COMMIT_REF_NAME}-test-unit-${test_group}/" \
        && populate_storage "/${CI_COMMIT_REF_NAME}-test-unit-${test_group}" \
        && pushd integrates \
        && PYTHONPATH="back/src/:back/migrations/:$PYTHONPATH" \
        && BATCH_BIN="$(command -v integrates-batch)" \
        && pytest -m 'not changes_db' "${pytest_args[@]}" back/test/unit/src \
        && popd \
        || return 1
    elif [ "$test_group" = "changes_db" ]; then
      DAEMON=true integrates-db \
        && export AWS_S3_PATH_PREFIX="${CI_COMMIT_REF_NAME}-test-unit-${test_group}/" \
        && populate_storage "/${CI_COMMIT_REF_NAME}-test-unit-${test_group}" \
        && pushd integrates \
        && PYTHONPATH="back/src/:back/migrations/:$PYTHONPATH" \
        && BATCH_BIN="$(command -v integrates-batch)" \
        && pytest -m 'changes_db' "${pytest_args[@]}" back/test/unit/src \
        && popd \
        || return 1
    else
      echo "\$ Error, $test_group is not a valid argument" \
        && exit 1
    fi
}

main "${@}"
