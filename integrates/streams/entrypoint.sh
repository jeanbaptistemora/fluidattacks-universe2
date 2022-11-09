# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash
function export_secrets {
  local env="${1}"
  local secrets=(
    AWS_OPENSEARCH_HOST
    AWS_REDSHIFT_DBNAME
    AWS_REDSHIFT_HOST
    AWS_REDSHIFT_PASSWORD
    AWS_REDSHIFT_USER
    BUGSNAG_API_KEY_STREAMS
    DYNAMODB_HOST
    DYNAMODB_PORT
    GOOGLE_CHAT_WEBHOOK_URL
    WEBHOOK_POC_KEY
    WEBHOOK_POC_ORG
    WEBHOOK_POC_URL
  )
  local secrets_path

  case "${env}" in
    dev) secrets_path=__argSecretsDev__ ;;
    prod-local) secrets_path=__argSecretsDev__ ;;
    prod) secrets_path=__argSecretsProd__ ;;
    *) error 'First argument must be one of: dev, prod, prod-local' ;;
  esac \
    && sops_export_vars "${secrets_path}" "${secrets[@]}" \
    || return 1
}

function get_stream_arn {
  local table="${1}"
  local aws_args=(--table-name "${table}")

  : \
    && if [ "${ENVIRONMENT}" = "dev" ]; then
      aws_args+=(--endpoint-url "${LOCAL_ENDPOINT}")
    fi \
    && aws dynamodbstreams list-streams "${aws_args[@]}" \
    | jq --raw-output ".Streams[0].StreamArn" \
    || return 1
}

function run_dynamodb_consumer {
  export LOCAL_ENDPOINT="http://${DYNAMODB_HOST}:${DYNAMODB_PORT}"

  local table="${1}"
  local name="${table}_consumer"
  local properties=(
    "applicationName = ${name}"
    "AWSCredentialsProvider = DefaultAWSCredentialsProviderChain"
    "executableName = python3 invoker.py dynamodb"
    "idleTimeBetweenReadsInMillis = 500"
    "initialPositionInStream = TRIM_HORIZON"
    "regionName = ${AWS_DEFAULT_REGION}"
    "streamName = $(get_stream_arn "${table}")"
  )
  local properties_file="${STATE}/${name}.properties"

  : \
    && if [ "${ENVIRONMENT}" = "dev" ]; then
      properties+=(
        "dynamoDBEndpoint = ${LOCAL_ENDPOINT}"
        "kinesisEndpoint = ${LOCAL_ENDPOINT}"
        "metricsLevel = NONE"
      )
    elif [ "${ENVIRONMENT}" = "prod-local" ]; then
      properties+=(
        "dynamoDBEndpoint = ${LOCAL_ENDPOINT}"
        "metricsLevel = NONE"
      )
    fi \
    && for property in "${properties[@]}"; do
      echo "${property}" >> "${properties_file}"
    done \
    && touch /tmp/healthy \
    && java \
      -Djava.util.logging.config.file="logging.properties" \
      "com.amazonaws.services.dynamodbv2.streamsadapter.StreamsMultiLangDaemon" \
      "${properties_file}" \
    || return 1
}

function main {
  export ENVIRONMENT="${1}"
  export AWS_DEFAULT_REGION="us-east-1"
  export CI_COMMIT_SHA

  echo "[INFO] Executing dynamodb streams consumer" \
    && export_secrets "${ENVIRONMENT}" \
    && if test -z "${CI_COMMIT_SHA:-}"; then
      CI_COMMIT_SHA="$(get_commit_from_rev . HEAD)"
    fi \
    && pushd __argSrc__ \
    && run_dynamodb_consumer integrates_vms \
    && popd \
    || return 1
}

main "${@}"
