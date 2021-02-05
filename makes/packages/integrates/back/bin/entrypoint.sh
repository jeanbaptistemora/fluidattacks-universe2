# shellcheck shell=bash

source '__envPypiRuntime__'
source '__envSearchPaths__'
source '__envTools__'
source '__envUtilsAws__'
source '__envUtilsSops__'

function main {
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
    --max-requests '64'
    # The maximum jitter to add to the max_requests setting. [0]
    --max-requests-jitter '32'
    # Workers silent for more than this many seconds are killed and restarted. [30]
    --timeout '300'
    # The type of workers to use. [sync]
    --worker-class 'back.settings.uvicorn.IntegratesWorker'
    # The maximum number of simultaneous clients. [1000]
    --worker-connections '512'
  )
  local secrets=(
    AZUREAD_OAUTH2_KEY
    AZUREAD_OAUTH2_SECRET
    BITBUCKET_OAUTH2_KEY
    BITBUCKET_OAUTH2_SECRET
    BUGSNAG_ACCESS_TOKEN
    BUGSNAG_API_KEY_SCHEDULER
    CLOUDFRONT_ACCESS_KEY
    CLOUDFRONT_PRIVATE_KEY
    CLOUDFRONT_REPORTS_DOMAIN
    CLOUDFRONT_RESOURCES_DOMAIN
    CLOUDMERSIVE_API_KEY
    COMMUNITY_PROJECTS
    DEBUG
    DEFAULT_ORG
    DYNAMODB_HOST
    DYNAMODB_PORT
    ENVIRONMENT
    GOOGLE_OAUTH2_KEY
    GOOGLE_OAUTH2_SECRET
    JWT_ENCRYPTION_KEY
    JWT_SECRET
    JWT_SECRET_API
    MAIL_CONTINUOUS
    MAIL_PRODUCTION
    MAIL_PROJECTS
    MAIL_RESOURCERS
    MAIL_REVIEWERS
    MANDRILL_APIKEY
    MIXPANEL_API_TOKEN
    REDIS_SERVER
    SQS_QUEUE_URL
    STARLETTE_SESSION_KEY
    TEST_PROJECTS
    ZENDESK_EMAIL
    ZENDESK_SUBDOMAIN
    ZENDESK_TOKEN
  )

      if test "${env}" == 'dev'
      then
            aws_login_dev 'integrates' \
        &&  sops_export_vars __envSecretsDev__ "${secrets[@]}" \
        &&  config+=(
              # SSL certificate file
              --certfile='__envCertsDevelopment__/cert.crt'
              # SSL key file
              --keyfile='__envCertsDevelopment__/cert.key'
              # The number of worker processes for handling requests
              --workers 3
            )
      elif test "${env}" == 'dev-mobile'
      then
            aws_login_dev 'integrates' \
        &&  sops_export_vars __envSecretsDev__ "${secrets[@]}" \
        &&  config+=(
              # The number of worker processes for handling requests
              --workers 3
            )
      elif test "${env}" == 'eph'
      then
            aws_login_dev 'integrates' \
        &&  sops_export_vars __envSecretsDev__ "${secrets[@]}" \
        &&  config+=(
              # The number of worker processes for handling requests
              --workers 3
            )
      elif test "${env}" == 'prod'
      then
            aws_login_prod 'integrates' \
        &&  sops_export_vars __envSecretsProd__ "${secrets[@]}" \
        &&  config+=(
              # The number of worker processes for handling requests
              --workers 5
            )
      else
            echo '[ERROR] First argument must be one of: dev, dev-mobile, eph, prod' \
        &&  return 1
      fi \
  &&  if ! test -e 'integrates'
      then
        # Kubernetes specific
            mkdir 'integrates' \
        &&  copy '__envIntegrates__' 'integrates'
      fi \
  &&  pushd integrates \
    &&  __envKillPidListeningOnPort__ "${port}" \
    &&  { STARTDIR="${PWD}" \
          __envAsgi__ "${config[@]}" 'back.app.app:APP' \
        & } \
    &&  __envWait__ 5 "${host}:${port}" \
    &&  __envDone__ 28001 \
    &&  echo '[INFO] Back is ready' \
    &&  wait \
  &&  popd \
  ||  return 1
}

main "${@}"
