# shellcheck shell=bash

function serve_daemon {
  kill_port 28001 \
    && { serve "${@}" & } \
    && wait_port 300 localhost:28001
}

function serve {
  local env="${1:-}"

  local config=(
    # The maximum number of pending connections. [2048]
    --backlog '512'
    # The socket to bind. [['127.0.0.1:8000']]
    --bind "${HOST}:${PORT}"
    # Front-end's IPs from which allowed to handle set secure headers. [127.0.0.1]
    --forwarded-allow-ips '*'
    # Timeout for graceful workers restart. [30]
    --graceful-timeout '30'
    # The maximum number of requests a worker will process before restarting. [0]
    --max-requests '256'
    # The maximum jitter to add to the max_requests setting. [0]
    --max-requests-jitter '64'
    # Workers silent for more than this many seconds are killed and restarted. [30]
    --timeout '300'
    # The type of workers to use. [sync]
    --worker-class 'settings.uvicorn.IntegratesWorker'
    # The maximum number of simultaneous clients. [1000]
    --worker-connections '512'
  )

  source __argIntegratesBackEnv__/template "${env}" \
    && case "${DAEMON:-}" in
      # The granularity of Error log outputs. [info]
      true) export LOG_LEVEL_CONSOLE="ERROR" ;;
      *) export LOG_LEVEL_CONSOLE="INFO" ;;
    esac \
    && if test "${env}" == 'dev'; then
      config+=(
        # SSL certificate file
        --certfile=__argCertsDevelopment__/cert.crt
        # SSL key file
        --keyfile=__argCertsDevelopment__/cert.key
        # The number of worker processes for handling requests
        --workers 1
      )
    elif test "${env}" == 'dev-mobile'; then
      config+=(
        # The number of worker processes for handling requests
        --workers 1
      )
    elif test "${env}" == 'eph'; then
      config+=(
        # The number of worker processes for handling requests
        --workers 3
      )
    elif test "${env}" == 'prod'; then
      config+=(
        # The number of worker processes for handling requests
        --workers 5
      )
    elif test "${env}" == 'prod-local'; then
      config+=(
        # SSL certificate file
        --certfile=__argCertsDevelopment__/cert.crt
        # SSL key file
        --keyfile=__argCertsDevelopment__/cert.key
        # The number of worker processes for handling requests
        --workers 3
      )
    else
      error First argument must be one of: dev, dev-mobile, eph, prod, prod-local
    fi \
    && pushd integrates \
    && kill_port "${PORT}" \
    && { gunicorn "${config[@]}" 'app.app:APP' & } \
    && wait_port 5 "${HOST}:${PORT}" \
    && done_port "${HOST}" 28001 \
    && info Back is ready \
    && wait \
    && popd \
    || return 1
}

function main {
  export HOST="${HOST:-0.0.0.0}"
  export PORT="${PORT:-8001}"
  export DAEMON="${DAEMON:-false}"

  case "${DAEMON:-}" in
    true) serve_daemon "${@}" ;;
    *) serve "${@}" ;;
  esac
}
main "${@}"
