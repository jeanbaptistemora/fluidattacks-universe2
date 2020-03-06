#!/usr/bin/env bash

reg_registry_id() {

  # Get the id of a gitlab registry
  # e.g reg_registry_id deps-base

  set -e

  local REGISTRY_NAME
  local INTEGRATES_ID
  local CHECK_URL

  REGISTRY_NAME="$1"
  INTEGRATES_ID='4620828'
  CHECK_URL="https://gitlab.com/api/v4/projects/$INTEGRATES_ID/registry/repositories"

  wget -O - "$CHECK_URL" 2> /dev/null | jq ".[] | select (.name == \"$REGISTRY_NAME\") | .id"
}

reg_registry_delete() {

  # Delete registry
  # e.g: reg_registry_delete deps-production TOKEN

  set -e

  REGISTRY_NAME="$1"
  TOKEN="$2"

  INTEGRATES_ID='4620828'
  REGISTRY_ID=$(reg_registry_id "$REGISTRY_NAME")
  DELETE_URL="https://gitlab.com/api/v4/projects/4620828/registry/repositories/$REGISTRY_ID"

  curl --request DELETE --header "PRIVATE-TOKEN: $TOKEN" "$DELETE_URL"
}

mobile_get_version() {

  # Get the current version for a mobile deployment

  set -e

  MINUTES=$(
    printf "%05d" $((
    ($(date +%d | sed 's/^0//') -1) * 1440 +
    $(date +%H | sed 's/^0//') * 60 +
    $(date +%M | sed 's/^0//')
    ))
  )
  if [ "$1" = "basic" ]; then
    FI_VERSION="$(date +%y.%m.)$MINUTES"
    echo "$FI_VERSION"
  elif [ "$1" = "code" ]; then
    FI_VERSION="$(date +%y%m)$MINUTES"
    echo "$FI_VERSION"
  else
    echo "Error. Only basic or code allowed as params"
    exit 1
  fi
}

commitlint_conf () {

  # download commitlint's configuration files

  set -e

  RULES_NAME='commitlint.config.js'
  PARSER_NAME='parser-preset.js'
  BRANCH='master'
  BASE_URL="https://static-objects.gitlab.net/fluidattacks/public/raw/$BRANCH/commitlint-configs/others"

  RULES_URL="$BASE_URL/$RULES_NAME"
  PARSER_URL="$BASE_URL/$PARSER_NAME"

  curl $RULES_URL > $RULES_NAME 2> /dev/null
  curl $PARSER_URL > $PARSER_NAME 2> /dev/null

}

minutes_of_month () {

  # Returns minutes that have passed during the current month

  set -e


  local MINUTES_OF_PASSED_DAYS
  local MINUTES_OF_PASSED_HOURS
  local MINUTES_OF_CURRENT_HOUR

  # Number of minutes from all days that have completely passed.
  MINUTES_OF_PASSED_DAYS=$((
    ($(date +%d | sed 's/^0//') -1) * 1440
  ))

  # Number of minutes from passed today's passed hours
  MINUTES_OF_PASSED_HOURS=$((
    $(date +%H | sed 's/^0//') * 60
  ))

  # Number of minutes that have passed during current hour
  MINUTES_OF_CURRENT_HOUR=$((
    $(date +%M | sed 's/^0//')
  ))

  # Total number of minutes that have passed since the beggining of the month
  MINUTES_OF_MONTH=$((
    $MINUTES_OF_PASSED_DAYS +
    $MINUTES_OF_PASSED_HOURS +
    $MINUTES_OF_CURRENT_HOUR
  ))

  echo "$MINUTES_OF_MONTH"
}

app_version () {

  # Return a version for integrates app

  set -e

  MINUTES=$(minutes_of_month)
  echo "$(date +%y.%m.)${MINUTES}"
}
