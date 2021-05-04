# shellcheck shell=bash

function main {
  local api_status="${2:-}"
  local env="${1:-}"
  local host='0.0.0.0'
  local port='8001'
  local config=(
    # The maximum number of pending connections. [2048]
    --backlog '512'
    # The socket to bind. [['127.0.0.1:8000']]
    --bind "${host}:${port}"
    # Front-end's IPs from which allowed to handle set secure headers. [127.0.0.1]
    --forwarded-allow-ips '*'
    # Timeout for graceful workers restart. [30]
    --graceful-timeout '30'
    # The granularity of Error log outputs. [info]
    --log-level 'info'
    # The maximum number of requests a worker will process before restarting. [0]
    --max-requests '256'
    # The maximum jitter to add to the max_requests setting. [0]
    --max-requests-jitter '64'
    # Workers silent for more than this many seconds are killed and restarted. [30]
    --timeout '300'
    # The type of workers to use. [sync]
    --worker-class 'back.settings.uvicorn.IntegratesWorker'
    # The maximum number of simultaneous clients. [1000]
    --worker-connections '512'
  )

      source __envIntegratesEnv__ "${env}" "${api_status}"\
  &&  if test "${env}" == 'dev'
      then
        config+=(
          # SSL certificate file
          --certfile='__envCertsDevelopment__/cert.crt'
          # SSL key file
          --keyfile='__envCertsDevelopment__/cert.key'
          # The number of worker processes for handling requests
          --workers 3
        )
      elif test "${env}" == 'dev-mobile'
      then
        config+=(
          # The number of worker processes for handling requests
          --workers 3
        )
      elif test "${env}" == 'eph'
      then
        config+=(
          # The number of worker processes for handling requests
          --workers 3
        )
      elif test "${env}" == 'prod'
      then
        config+=(
          # The number of worker processes for handling requests
          --workers 5
        )
      else
            echo '[ERROR] First argument must be one of: dev, dev-mobile, eph, prod' \
        &&  return 1
      fi \
  &&  pushd integrates \
    &&  makes-kill-port "${port}" \
    &&  { gunicorn "${config[@]}" 'back.app.app:APP' & } \
    &&  makes-wait 5 "${host}:${port}" \
    &&  makes-done 28001 \
    &&  echo '[INFO] Back is ready' \
    &&  wait \
  &&  popd \
  ||  return 1
}

main "${@}"
