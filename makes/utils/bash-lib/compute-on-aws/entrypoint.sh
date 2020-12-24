#! __envShell__
# shellcheck shell=bash

source '__makeEntrypoint__'
source '__envUtilsBashLibAws__'

function main {
  local manifest='__envManifest__'

      echo '[INFO] Running on AWS: __envCommand__' \
  &&  echo '[INFO] VCPUs: __envVcpus__' \
  &&  echo '[INFO] Memory: __envMemory__ MB' \
  &&  echo '[INFO] Attempts: __envAttempts__' \
  &&  echo '[INFO] Timeout: __envTimeout__ seconds' \
  &&  echo '[INFO] Job Name: __envJobname__' \
  &&  echo '[INFO] Job Queue: __envJobqueue__' \
  &&  aws_login_prod '__envProduct__' \

}

main "${@}"
