# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"

function job_run_dynamodb_local {
  local port=8022

      echo '[INFO] Launching DynamoDB local' \
  &&  {
        java \
          -Djava.library.path=./.DynamoDB/DynamoDBLocal_lib \
          -jar ./.DynamoDB/DynamoDBLocal.jar \
          -inMemory \
          -port "${port}" \
          -sharedDb \
        &
      } \
  &&  echo '[INFO] Waiting 5 seconds to leave DynamoDB start' \
  &&  sleep 5 \
  &&  echo '[INFO] Populating DynamoDB local' \
  &&  bash ./deploy/containers/common/vars/provision_local_db.sh \
  &&  echo "[INFO] DynamoDB is ready and listening on port ${port}!" \
  &&  echo "[INFO] Hit Ctrl+C to exit" \
  &&  fg %1
}
