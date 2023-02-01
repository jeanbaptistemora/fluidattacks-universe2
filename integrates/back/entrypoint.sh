# shellcheck shell=bash

function serve_daemon {
  kill_port 28001 \
    && { serve "${@}" & } \
    && wait_port 300 localhost:28001
}

function serve {
  local env="${1:-}"
  # https://docs.gunicorn.org/en/latest/design.html#how-many-workers
  local recommended_workers
  local config=(
    # The socket to bind. [['127.0.0.1:8000']]
    --bind "${HOST}:${PORT}"
    # The Gunicorn config file
    --config 'python:settings.gunicorn'
    # Front-end's IPs from which allowed to handle set secure headers. [127.0.0.1]
    --forwarded-allow-ips '*'
    # Workers silent for more than this many seconds are killed and restarted. [30]
    --timeout '120'
    # The type of workers to use. [sync]
    --worker-class 'settings.uvicorn.IntegratesWorker'
  )
  # The current value of alb.ingress.kubernetes.io/load-balancer-attributes is set to 120
  # but we wait a little longer to let the ALB close the connection first
  # which is important to prevent some 5XX responses
  local load_balancer_timeout=125

  source __argIntegratesBackEnv__/template "${env}" \
    && case "${DAEMON:-}" in
      # The granularity of Error log outputs. [info]
      true) export LOG_LEVEL_CONSOLE="ERROR" ;;
      *) export LOG_LEVEL_CONSOLE="INFO" ;;
    esac \
    && recommended_workers=$(python3 -c "import os; print(2 * os.cpu_count() + 1)") \
    && if test "${env}" == 'dev'; then
      config+=(
        # SSL certificate file
        --certfile=__argCertsDevelopment__/cert.crt
        # SSL key file
        --keyfile=__argCertsDevelopment__/cert.key
        # Restart workers when code changes
        --reload
        # The number of worker processes for handling requests
        --workers 1
      )
    elif test "${env}" == 'eph'; then
      config+=(
        # The number of seconds to wait for requests on a Keep-Alive connection
        --keep-alive "${load_balancer_timeout}"
        # The number of worker processes for handling requests
        --workers "${recommended_workers}"
      )
    elif test "${env}" == 'prod'; then
      config+=(
        # The number of seconds to wait for requests on a Keep-Alive connection
        --keep-alive "${load_balancer_timeout}"
        # The number of worker processes for handling requests
        --workers "${recommended_workers}"
      )
    elif test "${env}" == 'prod-local'; then
      config+=(
        # SSL certificate file
        --certfile=__argCertsDevelopment__/cert.crt
        # SSL key file
        --keyfile=__argCertsDevelopment__/cert.key
        # Restart workers when code changes
        --reload
        # The number of worker processes for handling requests
        --workers 1
      )
    else
      error First argument must be one of: dev, eph, prod, prod-local
    fi \
    && pushd integrates/back/src \
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
