# shellcheck shell=bash

function dynamo_forces {
  local conf

  conf="./observes/conf/awsdynamodb_forces.json" \
    && observes-job-dynamodb-etl "${conf}" "dynamodb_forces"
}

dynamo_forces
