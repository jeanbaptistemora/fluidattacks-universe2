#!/bin/bash

aws dynamodb create-table --endpoint-url http://localhost:8022 \
  --table-name 'fi_authorization' \
  --billing-mode 'PAY_PER_REQUEST' \
  --attribute-definitions '[{
      "AttributeName": "id",
      "AttributeType": "S"
    },{
      "AttributeName": "rule_subject",
      "AttributeType": "S"
    },{
      "AttributeName": "rule_object",
      "AttributeType": "S"
    }]' \
  --key-schema '[{
      "AttributeName": "id",
      "KeyType": "HASH"
    }]' \
  --global-secondary-indexes '[{
      "IndexName": "subject_policies",
      "KeySchema": [{
        "AttributeName": "rule_subject",
        "KeyType": "HASH"
      },{
        "AttributeName": "rule_object",
        "KeyType": "RANGE"
      }],
      "Projection": {
        "ProjectionType": "ALL"
      }
    }]'

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
--global-secondary-indexes \
    IndexName=project_access_users,\
KeySchema=["{AttributeName=project_name,KeyType=HASH}"],\
Projection="{ProjectionType=KEYS_ONLY}",ProvisionedThroughput="{ReadCapacityUnits=10,WriteCapacityUnits=10}" \
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

aws dynamodb create-table --endpoint-url http://localhost:8022 \
--table-name fi_project_names \
--attribute-definitions AttributeName=project_name,AttributeType=S \
--key-schema AttributeName=project_name,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

aws dynamodb create-table \
    --endpoint-url \
        http://localhost:8022 \
    --table-name \
        bb_executions \
    --attribute-definitions \
        AttributeName=subscription,AttributeType=S \
        AttributeName=execution_id,AttributeType=S \
    --key-schema \
        AttributeName=subscription,KeyType=HASH \
        AttributeName=execution_id,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=1,WriteCapacityUnits=1

for mock_file in test/dynamo_data/*.json; do
    echo "[INFO] Writing data from: ${mock_file}"
    aws dynamodb batch-write-item --endpoint-url http://localhost:8022 \
    --request-items file://${mock_file}
done

iso_date_now=$(date +%Y-%m-%dT%H:%M:%S.000000%z)

# This will insert two extra rows with current date-time
# This rows are always visible in the front-end :)
sed "s/2020-02-19.*/${iso_date_now}\"/g" \
  < 'test/dynamo_data/bb_executions.json' \
  | sed "s/33e5d863252940edbfb144ede56d56cf/aaa/g" \
  | sed "s/a125217504d447ada2b81da3e4bdab0e/bbb/g" \
  > test/dynamo_data/bb_executions.json.now

echo '[INFO] Writing data from: test/dynamo_data/bb_executions.json.now'
aws dynamodb batch-write-item \
  --endpoint-url 'http://localhost:8022' \
  --request-items 'file://test/dynamo_data/bb_executions.json.now'
