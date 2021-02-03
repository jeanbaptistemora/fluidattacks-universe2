# shellcheck shell=bash

function main {
  local host='127.0.0.1'
  local port='8022'
  local state_path='integrates/.DynamoDB'

      echo '[INFO] Unpacking DynamoDB' \
  &&  rm -rf "${state_path}" \
  &&  mkdir -p "${state_path}" \
  &&  pushd "${state_path}" \
    &&  __envUnzip__ -u '__envDynamoZip__' \
  &&  popd \
  &&  echo '[INFO] Deleting old instance, if exists' \
  &&  __envKillPidListeningOnPort__ "${port}" \
  &&  echo '[INFO] Launching DynamoDB' \
  &&  { __envJava__ \
          -Djava.library.path="${state_path}/DynamoDBLocal_lib" \
          -jar "${state_path}/DynamoDBLocal.jar" \
          -inMemory \
          -port "${port}" \
          -sharedDb \
      & } \
  &&  __envWait__ 10 "${host}:${port}" \
  &&  copy __envTerraformModule__ "${state_path}/terraform" \
  &&  pushd "${state_path}/terraform" \
    &&  __envTerraform__ init \
    &&  __envTerraform__ apply -auto-approve \
  &&  popd \
  &&  for data in '__envDynamoData__/'*'.json'
      do
            echo "[INFO] Writing data from: ${data}" \
        &&  __envAws__ dynamodb batch-write-item \
              --endpoint-url "http://${host}:${port}" \
              --request-items "file://${data}" \
        ||  return 1
      done \
  &&  echo '[INFO] Dynamo DB is ready' \
  &&  wait
}

main "${@}"
