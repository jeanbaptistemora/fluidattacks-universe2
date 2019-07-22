#!/usr/bin/env bash

kaniko_build() {

  # This scripts builds a Dockerfile using kaniko with cache
  # and pushes to the registry if the branch is master

  echo "{\"auths\":{\"${CI_REGISTRY}\":{\"username\":\"${CI_REGISTRY_USER}\",\
    \"password\":\"${CI_REGISTRY_PASSWORD}\"}}}" > /kaniko/.docker/config.json

  if [[ "$CI_COMMIT_REF_NAME" == "master" ]]; then
    /kaniko/executor \
      --cleanup \
      --context "${CI_PROJECT_DIR}" \
      --dockerfile "deploy/containers/$1/Dockerfile" \
      --destination "${CI_REGISTRY_IMAGE}:$1" \
      --cache=true \
      --cache-repo "${CI_REGISTRY_IMAGE}/cache/$1" \
      --snapshotMode time
  else
    /kaniko/executor \
      --cleanup \
      --context "${CI_PROJECT_DIR}" \
      --dockerfile "deploy/containers/$1/Dockerfile" \
      --no-push \
      --cache=true \
      --cache-repo "${CI_REGISTRY_IMAGE}/cache/$1" \
      --snapshotMode time
  fi
}

mobile_get_version() {

  # Gets the current version for a mobile deployment

  MINUTES=$(
    printf "%05d" $((
    ($(date +%d | sed 's/^0//') -1) * 1440 +
    $(date +%H | sed 's/^0//') * 60 +
    $(date +%M | sed 's/^0//')
    ))
  )
  if [[ "$1" == "basic" ]]; then
    FI_VERSION="$(date +%y.%m.)${MINUTES}"
    echo "$FI_VERSION"
  elif [[ "$1" == "code" ]]; then
    FI_VERSION="$(date +%y%m)${MINUTES}"
    echo "$FI_VERSION"
  else
    echo "Error. Only basic or code allowed as params"
    exit 1
  fi
}

commitlint_conf () {

  #This scripts download commitlint's configuration files

  local RULES_NAME
  local PARSER_NAME
  local BRANCH
  local BASE_URL
  local RULES_URL
  local PARSER_URL

  RULES_NAME='commitlint.config.js'
  PARSER_NAME='parser-preset.js'
  BRANCH='master'
  BASE_URL="https://gitlab.com/fluidattacks/default/raw/$BRANCH/commitlint-configs/others"

  RULES_URL="$BASE_URL/$RULES_NAME"
  PARSER_URL="$BASE_URL/$PARSER_NAME"

  curl $RULES_URL > $RULES_NAME 2> /dev/null
  curl $PARSER_URL > $PARSER_NAME 2> /dev/null

}
