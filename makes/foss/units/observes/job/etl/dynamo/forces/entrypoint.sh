# shellcheck shell=bash

alias dynamodb-etl="observes-etl-dynamo"

function dynamo_forces {
  local conf

  conf="./observes/conf/awsdynamodb_forces.json" \
    && dynamodb-etl "${conf}" "dynamodb_forces"
}

dynamo_forces
