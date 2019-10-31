#!/bin/bash

aws dynamodb create-table --endpoint-url http://localhost:8022 \
--table-name FI_findings \
--attribute-definitions \
    AttributeName=finding_id,AttributeType=S \
    AttributeName=project_name,AttributeType=S \
--key-schema AttributeName=finding_id,KeyType=HASH \
--global-secondary-indexes \
    IndexName=project_findings,\
KeySchema=["{AttributeName=project_name,KeyType=HASH}"],\
Projection="{ProjectionType=INCLUDE,NonKeyAttributes=["releaseDate"]}",\
ProvisionedThroughput="{ReadCapacityUnits=10,WriteCapacityUnits=10}" \
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
--attribute-definitions \
    AttributeName=event_id,AttributeType=S \
    AttributeName=project_name,AttributeType=S \
--key-schema \
    AttributeName=event_id,KeyType=HASH \
--global-secondary-indexes \
    IndexName=project_events,\
KeySchema=["{AttributeName=project_name,KeyType=HASH}"],\
Projection="{ProjectionType=KEYS_ONLY}",ProvisionedThroughput="{ReadCapacityUnits=10,WriteCapacityUnits=10}" \
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
