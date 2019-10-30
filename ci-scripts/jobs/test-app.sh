#!/usr/bin/env bash

# Runs linters and unit tests on app

# Linters
run_lint () {
    set -e
    prospector -F -s high -u django -i node_modules app/
    prospector -F -s veryhigh -u django -i node_modules fluidintegrates/
}

provision_mock () {
    service redis-server start

    aws configure set aws_access_key_id ${FI_AWS_DYNAMODB_ACCESS_KEY}
    aws configure set aws_secret_access_key ${FI_AWS_DYNAMODB_SECRET_KEY}
    aws configure set region us-east-1

    java -Djava.library.path=/usr/local/lib/dynamodb-local/DynamoDBLocal_lib \
        -jar /usr/local/lib/dynamodb-local/DynamoDBLocal.jar \
        -sharedDb \
        -port 8022 &
    DYNAMODB_PROCESS=$!

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name FI_findings \
    --attribute-definitions AttributeName=finding_id,AttributeType=S \
    --key-schema AttributeName=finding_id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name FI_alerts_by_company \
    --attribute-definitions \
        AttributeName=company_name,AttributeType=S \
        AttributeName=project_name,AttributeType=S \
    --key-schema \
        AttributeName=company_name,KeyType=HASH \
        AttributeName=project_name,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name FI_comments \
    --attribute-definitions \
        AttributeName=finding_id,AttributeType=N \
        AttributeName=user_id,AttributeType=N \
    --key-schema \
        AttributeName=finding_id,KeyType=HASH \
        AttributeName=user_id,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name fi_events \
    --attribute-definitions AttributeName=event_id,AttributeType=S \
    --key-schema AttributeName=event_id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name FI_project_access \
    --attribute-definitions \
        AttributeName=user_email,AttributeType=S \
        AttributeName=project_name,AttributeType=S \
    --key-schema \
        AttributeName=user_email,KeyType=HASH \
        AttributeName=project_name,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name fi_project_comments \
    --attribute-definitions \
        AttributeName=project_name,AttributeType=S \
        AttributeName=user_id,AttributeType=N \
    --key-schema \
        AttributeName=project_name,KeyType=HASH \
        AttributeName=user_id,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name FI_projects \
    --attribute-definitions AttributeName=project_name,AttributeType=S \
    --key-schema AttributeName=project_name,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name FI_toe \
    --attribute-definitions AttributeName=project,AttributeType=S \
    --key-schema AttributeName=project,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name FI_users \
    --attribute-definitions AttributeName=email,AttributeType=S \
    --key-schema AttributeName=email,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    aws dynamodb create-table --endpoint-url http://localhost:8022 \
    --table-name FI_vulnerabilities \
    --attribute-definitions \
        AttributeName=finding_id,AttributeType=S \
        AttributeName=UUID,AttributeType=S \
    --key-schema \
        AttributeName=finding_id,KeyType=HASH \
        AttributeName=UUID,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

    for mock_file in app/test/dynamo_data/*.json; do
        aws dynamodb batch-write-item --endpoint-url http://localhost:8022 \
        --request-items file://${mock_file}
    done
}

run_unit_test () {
    # Unit tests
    cp -a "$PWD" /usr/src/app_src
    cd /usr/src/app_src || return 1
    mkdir -p build/test
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

    cd "$CI_PROJECT_DIR" || RETVAL=1
    return $RETVAL
}

teardown () {
    kill -9 $DYNAMODB_PROCESS || true
    rm -f shared-local-instance.db
}

run_lint
provision_mock
run_unit_test || exit 1
teardown