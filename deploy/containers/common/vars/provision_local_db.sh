#!/bin/bash

aws dynamodb create-table \
  --attribute-definitions '[{
      "AttributeName": "subject",
      "AttributeType": "S"
    },{
      "AttributeName": "object",
      "AttributeType": "S"
    }]' \
  --billing-mode 'PAY_PER_REQUEST' \
  --endpoint-url http://localhost:8022 \
  --key-schema '[{
      "AttributeName": "subject",
      "KeyType": "HASH"
    },{
      "AttributeName": "object",
      "KeyType": "RANGE"
    }]' \
  --table-name 'fi_authz' \

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
--table-name fi_portfolios \
--attribute-definitions \
    AttributeName=organization,AttributeType=S \
    AttributeName=tag,AttributeType=S \
--key-schema \
    AttributeName=organization,KeyType=HASH \
    AttributeName=tag,KeyType=RANGE \
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

for mock_file in test_async/dynamo_data/*.json; do
    echo "[INFO] Writing data from: ${mock_file}"
    aws dynamodb batch-write-item --endpoint-url http://localhost:8022 \
    --request-items file://${mock_file}
done

iso_date_now=$(date +%Y-%m-%dT%H:%M:%S.000000%z)

# This will insert two extra rows with current date-time
# This rows are always visible in the front-end :)
sed "s/2020-02-19.*/${iso_date_now}\"/g" \
  < 'test_async/dynamo_data/bb_executions.json' \
  | sed "s/33e5d863252940edbfb144ede56d56cf/aaa/g" \
  | sed "s/a125217504d447ada2b81da3e4bdab0e/bbb/g" \
  > test_async/dynamo_data/bb_executions.json.now

echo '[INFO] Writing data from: test_async/dynamo_data/bb_executions.json.now'
aws dynamodb batch-write-item \
  --endpoint-url 'http://localhost:8022' \
  --request-items 'file://test_async/dynamo_data/bb_executions.json.now'

if test "${CI_JOB_NAME:-}" = "serve_dynamodb_local"
then
  echo '[INFO] Adding mock users'
  for index in $(seq 1 200)
  do
    echo "  [INFO] adding 6 users, batch ${index} out of 200"
    index="${index}" jq -n '{
      "FI_users": (
        [range(6)] | map([{
          "PutRequest": {
            "Item" : {
              "company": {"S": "unittest"},
              "date_joined": {"S": "2018-02-28 11:54:12"},
              "email": {"S": "mock_user.index_\(env.index).batch_\(.)@gmail.com"},
              "legal_remember": {"BOOL": true},
              "registered": {"BOOL": true}
            }
          }
        }]) | flatten(2)
      ),
      "fi_authz": (
        [range(6)] | map([{
          "PutRequest": {
            "Item": {
              "level": {"S": "user"},
              "subject": {"S": "mock_user.index_\(env.index).batch_\(.)@gmail.com"},
              "object": {"S": "self"},
              "role": {"S": "customer"}
            }
          }
        },{
          "PutRequest": {
            "Item": {
              "level": {"S": "group"},
              "subject": {"S": "mock_user.index_\(env.index).batch_\(.)@gmail.com"},
              "object": {"S": "oneshottest"},
              "role": {"S": "customer"}
            }
          }
        }]) | flatten(2)
      ),
      "FI_project_access": (
        [range(6)] | map([{
          "PutRequest": {
            "Item": {
              "responsibility": {
                "S": "mock"
              },
              "project_name": {
                "S": "oneshottest"
              },
              "has_access": {
                "BOOL": true
              },
              "user_email": {
                "S": "mock_user.index_\(env.index).batch_\(.)@gmail.com"
              }
            }
          }
        }]) | flatten(2)
      )
    }' > .tmp
    aws dynamodb batch-write-item \
      --endpoint-url 'http://localhost:8022' \
      --request-items 'file://.tmp'
  done
fi

if test "${CI_JOB_NAME:-}" != "test_back"
then
  number_findings=()
  number_vulns=()
  for index in {0..45}
  do
    number_findings+=($((RANDOM%5+1)))
    number_vulns+=($((RANDOM%3+1)))
  done
  echo '[INFO] Adding mock projects'
  for index in $(seq 1 45)
  do
    echo "  [INFO] adding project, ${index} out of 45"
    index="${index}" jq --argjson n_findings "${number_findings[index]}" \
      --argjson n_vulns "${number_vulns[index]}" -n '{
      "FI_projects": ([
        {
          "PutRequest" : {
            "Item" : {
              "companies" : {
                "L" : [
                  {
                    "S": "unittest"
                  }
                ]
              },
              "description" : {
                "S" : "mock project index_\(env.index)"
              },
              "hasRelease" : {
                "BOOL" : true
              },
              "last_closing_date" : {
                "N" : "45"
              },
              "max_open_severity" : {
                "N" : "3.9"
              },
              "mean_remediate" : {
                "N" : "73"
              },
              "mean_remediate_critical_severity" : {
                "N" : "83"
              },
              "mean_remediate_high_severity" : {
                "N" : "93"
              },
              "mean_remediate_low_severity" : {
                "N" : "103"
              },
              "mean_remediate_medium_severity" : {
                "N" : "113"
              },
              "project_name" : {
                "S" : "project\(env.index)"
              },
              "project_status" : {
                "S" : "ACTIVE"
              },
              "tag" : {
                "SS" : [
                  "test-tag"
                ]
              },
              "total_treatment" : {
                "M" : {
                  "accepted" : {
                    "N" : "0"
                  },
                  "acceptedUndefined": {
                    "N": "0"
                  },
                  "inProgress" : {
                    "N" : "0"
                  },
                  "undefined" : {
                    "N" : "\(($n_findings * $n_vulns / 2) | floor)"
                  }
                }
              },
              "type" : {
                "S" : "continuous"
              }
            }
          }
        }]
      ),
      "fi_authz": ([
        {
          "PutRequest": {
            "Item": {
              "level": {"S": "group"},
              "subject": {"S": "integratesuser@gmail.com"},
              "object": {"S": "project\(env.index)"},
              "role": {"S": "customer"}
            }
          }
        }]
      ),
      "FI_project_access": ([
        {
          "PutRequest": {
            "Item": {
              "responsibility": {
                "S": "mock"
              },
              "project_name": {
                "S": "project\(env.index)"
              },
              "has_access": {
                "BOOL": true
              },
              "user_email": {
                "S": "integratesuser@gmail.com"
              }
            }
          }
        }]
      ),
      "FI_findings": (
        [range($n_findings)] | map([{
          "PutRequest": {
            "Item": {
              "integrity_impact": {
                "N": "0.22"
              },
              "integrity_requirement": {
                "N": "1"
              },
              "modified_severity_scope": {
                "N": "0"
              },
              "report_confidence": {
                "N": "0.96"
              },
              "project_name": {
                "S": "project\(env.index)"
              },
              "privileges_required": {
                "N": "0.85"
              },
              "availability_impact": {
                "N": "0.22"
              },
              "historic_state": {
                "L": [
                  {
                    "M": {
                      "date": {
                        "S": "2019-04-07 19:43:18"
                      },
                      "analyst": {
                        "S":"integratesmanager@gmail.com"
                      },
                      "state": {
                        "S":"CREATED"
                      }
                    }
                  },
                  {
                    "M": {
                      "date": {
                        "S": "2019-04-07 19:45:11"
                      },
                      "analyst": {
                        "S":"integratesmanager@gmail.com"
                      },
                      "state": {
                        "S":"SUBMITTED"
                      }
                    }
                  },
                  {
                    "M": {
                      "date": {
                        "S": "2019-04-07 19:45:15"
                      },
                      "analyst": {
                        "S":"integratesmanager@gmail.com"
                      },
                      "state": {
                        "S":"APPROVED"
                      }
                    }
                  }
                ]
              },
              "modified_privileges_required": {
                "N": "0.62"
              },
              "modified_attack_vector": {
                "N": "0.55"
              },
              "confidentiality_impact": {
                "N": "0.22"
              },
              "remediation_level": {
                "N": "0.95"
              },
              "availability_requirement": {
                "N": "0.5"
              },
              "report_date": {
                "S":"2019-04-07 19:45:11"
              },
              "attack_complexity": {
                "N": "0.77"
              },
              "finding_id": {
                "S": "988493\(.)\(env.index | tonumber + 10)"
              },
              "requirements": {
                "S": "REQ.0266. La organización debe deshabilitar las funciones inseguras de un sistema. (hardening de sistemas)"
              },
              "effect_solution": {
                "S": "-"
              },
              "releaseDate": {
                "S": "2019-04-07 19:45:15"
              },
              "modified_confidentiality_impact": {
                "N": "0"
              },
              "cvss_temporal": {
                "N": "6.3"
              },
              "modified_user_interaction": {
                "N": "0.85"
              },
              "modified_availability_impact": {
                "N": "0"
              },
              "modified_integrity_impact": {
                "N": "0"
              },
              "vulnerability": {
                "S": "Funcionalidad insegura description"
              },
              "finding": {
                "S": "FIN.S.0014. Funcionalidad insegura"
              },
              "finding_type": {
                "S": "SECURITY"
              },
              "attack_vector": {
                "N": "0.85"
              },
              "modified_attack_complexity": {
                "N": "0.77"
              },
              "cwe": {
                "S": "749"
              },
              "cvss_version": {
                "S": "3.1"
              },
              "cvss_env": {
                "N": "0.0"
              },
              "lastVulnerability": {
                "S": "2019-04-07 19:45:15"
              },
              "confidentiality_requirement": {
                "N": "1.5"
              },
              "user_interaction": {
                "N": "0.85"
              },
              "historic_treatment": {
                "L": [
                  {
                    "M": {
                      "date": {
                        "S": "2019-04-07 19:43:18"
                      },
                      "treatment": {
                        "S": "NEW"
                      },
                      "user": {
                        "S": "integratesmanager@gmail.com"
                      }
                    }
                  }
                ]
              },
              "cvss_basescore": {
                "N": "7.3"
              },
              "files": {
                "L": [
                {
                  "M": {
                      "name": {
                        "S":"exploitation"
                      },
                      "file_url": {
                        "S":"unittesting-988493279-exploitation.png"
                      }
                    }
                  }
                ]
              },
              "analyst": {
                "S": "integratesmanager@gmail.com"
              },
              "exploitability": {
                "N": "0.94"
              },
              "severity_scope": {
                "N": "0"
              }
            }
          }
        }]) | flatten(2)
      ),
      "FI_vulnerabilities": (
        [range($n_findings * $n_vulns)] | map([{
          "PutRequest" : {
            "Item" : {
              "UUID" : {
                "S" : "69b84d52-1b18-41fa-84b5-bcb8134c\(. | tonumber + 10)\(env.index | tonumber + 10)"
              },
              "finding_id" : {
                "S" : "988493\(. | tonumber % $n_findings)\(env.index | tonumber + 10)"
              },
              "historic_state" : {
                "L" : [
                  {
                    "M" : {
                      "analyst" : {
                        "S" : "unittest@fluidattacks.com"
                      },
                      "date" : {
                        "S" : "2019-04-07 08:45:48"
                      },
                      "state" : {
                        "S" : "\(if . | tonumber % 2 == 0 then "closed" else "open" end)"
                      }
                    }
                  }
                ]
              },
              "specific" : {
                "S" : "9999"
              },
              "vuln_type" : {
                "S" : "ports"
              },
              "where" : {
                "S" : "192.168.1.20"
              }
            }
          }
        }]) | flatten(2)
      ),
    }' > .tmp
    aws dynamodb batch-write-item \
      --endpoint-url 'http://localhost:8022' \
      --request-items 'file://.tmp'
  done
fi
