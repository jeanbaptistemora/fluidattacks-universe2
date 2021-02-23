# shellcheck shell=bash

function serve {
  export AWS_ACCESS_KEY_ID='test'
  export AWS_SECRET_ACCESS_KEY='test'
  export AWS_DEFAULT_REGION='us-east-1'
  local host='127.0.0.1'
  local port='8022'
  local state_path='.DB'

      echo '[INFO] Unpacking DynamoDB' \
  &&  rm -rf "${state_path}" \
  &&  mkdir -p "${state_path}" \
  &&  pushd "${state_path}" \
    &&  __envUnzip__ -u '__envDynamoZip__' \
  &&  popd \
  &&  echo '[INFO] Deleting old instance, if exists' \
  &&  makes-kill-port "${port}" 28022 \
  &&  echo '[INFO] Launching DynamoDB' \
  &&  { __envJava__ \
          -Djava.library.path="${state_path}/DynamoDBLocal_lib" \
          -jar "${state_path}/DynamoDBLocal.jar" \
          -inMemory \
          -port "${port}" \
          -sharedDb \
      & } \
  &&  makes-wait 10 "${host}:${port}" \
  &&  copy __envTerraformModule__ "${state_path}/terraform" \
  &&  pushd "${state_path}/terraform" \
    &&  __envTerraform__ init \
    &&  __envTerraform__ apply -auto-approve \
  &&  popd \
  &&  __envSed__ "s/2020-09-04.*/$(date -u +%Y-%m-%dT%H:%M:%S.000000%z)\"/g" \
        < '__envDynamoData__/forces.json' \
        | __envSed__ "s/33e5d863252940edbfb144ede56d56cf/aaa/g" \
        | __envSed__ "s/a125217504d447ada2b81da3e4bdab0e/bbb/g" \
        > "${state_path}/forces.now.json" \
  &&  for data in '__envDynamoData__/'*'.json' "${state_path}/"*'.json'
      do
            echo "[INFO] Writing data from: ${data}" \
        &&  __envAws__ dynamodb batch-write-item \
              --endpoint-url "http://${host}:${port}" \
              --request-items "file://${data}" \
        ||  return 1
      done \
  &&  makes-done 28022 \
  &&  echo '[INFO] Dynamo DB is ready' \
  &&  wait
}

function serve_daemon {
      makes-kill-port 28022 \
  &&  { serve "${@}" & } \
  &&  makes-wait 60 localhost:28022
}

function main {
  if test "${DAEMON:-}" = 'true'
  then
    serve_daemon "${@}"
  else
    serve "${@}"
  fi
}

main "${@}"
