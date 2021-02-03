# shellcheck shell=bash

function main {
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
  &&  __envWait__ 10 "127.0.0.1:${port}" \
  &&  wait
}

main "${@}"
