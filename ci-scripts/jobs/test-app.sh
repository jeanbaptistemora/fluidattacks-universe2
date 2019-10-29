#!/usr/bin/env bash

# Runs linters and unit tests on app

# Linters
run_lint () {
    set -e
    prospector -F -s high -u django -i node_modules app/
    prospector -F -s veryhigh -u django -i node_modules fluidintegrates/
}

run_unit_test () {
    # Unit tests
    cp -a "$PWD" /usr/src/app_src
    cd /usr/src/app_src || return 1
    mkdir -p build/test
    service redis-server start
    java -Djava.library.path=/usr/local/lib/dynamodb-local/DynamoDBLocal_lib -jar /usr/local/lib/dynamodb-local/DynamoDBLocal.jar -sharedDb -port 8022 &
    DYNAMODB_PROCESS=$!
    pytest \
    --ds=fluidintegrates.settings \
    -n auto \
    --dist=loadscope \
    --verbose \
    --exitfirst \
    --cov=fluidintegrates \
    --cov=app \
    --cov-report term \
    --cov-report html:build/coverage/html \
    --cov-report xml:build/coverage/results.xml \
    --cov-report annotate:build/coverage/annotate \
    --basetemp=build/test \
    --junitxml=build/test/results.xml \
    app/test/
    RETVAL=$?
    cp -a build/coverage/results.xml "$CI_PROJECT_DIR/coverage.xml"
    kill -9 $DYNAMODB_PROCESS || true
    cd "$CI_PROJECT_DIR" || RETVAL=1
    return $RETVAL
}

run_lint
run_unit_test || exit 1
