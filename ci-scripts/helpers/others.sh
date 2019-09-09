#!/usr/bin/env sh

reg_repo_id () {

  # Get the id of a gitlab registry repo

  #set -e

  INTEGRATES_ID='4620828'
  CHECK_URL="https://gitlab.com/api/v4/projects/$INTEGRATES_ID/registry/repositories"

  wget -O - "$CHECK_URL" 2> /dev/null | jq ".[] | select (.name == \"$1\") | .id"
}

reg_repo_tag_exists () {

  # Checks if a tag exists within a specific registry repository
  # Example: reg_repo_tag_exists deps-production master will return 0

  #set -e

  REPO_NAME=$1
  TAG_NAME=$2

  INTEGRATES_ID='4620828'
  REPO_ID=$(reg_repo_id "$REPO_NAME")
  CHECK_URL="https://gitlab.com/api/v4/projects/$INTEGRATES_ID/registry/repositories/$REPO_ID/tags/$TAG_NAME"
  TAG=$(wget -O - "$CHECK_URL" 2> /dev/null | jq -r '.name')

  if [ "$TAG" = "$TAG_NAME" ]; then
    echo "$REPO_NAME:$TAG_NAME exists"
    return 0
  else
    echo "$REPO_NAME:$TAG_NAME does not exist"
    return 1
  fi
}

kaniko_login() {
  echo "{\"auths\":{\"$CI_REGISTRY\":{\"username\":\"$CI_REGISTRY_USER\",\
    \"password\":\"$CI_REGISTRY_PASSWORD\"}}}" > /kaniko/.docker/config.json
}

kaniko_build() {

  # Build a Dockerfile using kaniko.
  # Pushes ephemeral images for devs if eph=true.
  # Uses cache if cache=true.
  # Additional kaniko parameters can be added if needed.
  # Example: kaniko_build mobile eph=false cache=true --build-arg VERSION='1.2'

  set -e

  TARGET="$1"
  USE_EPH="$2"
  USE_CACHE="$3"
  shift 3

  # Set cache parameter based on USE_EPH
  echo "Option: \"$USE_EPH\" specified."
  if [ "$USE_EPH" = 'eph=true' ]; then
    SET_EPH="--destination $CI_REGISTRY_IMAGE/$TARGET:$CI_COMMIT_REF_NAME"
  elif [ "$USE_EPH" = 'eph=false' ]; then
    if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
      SET_EPH="--destination $CI_REGISTRY_IMAGE/$TARGET:$CI_COMMIT_REF_NAME"
    else
      SET_EPH='--no-push'
    fi
  else
    echo 'Error. Either eph=true or eph=false must be specified for $3'
    return 1
  fi

  # Set destination parameter based on USE_CACHE
  echo "Option: \"$USE_CACHE\" specified."
  if [ "$USE_CACHE" = 'cache=true' ]; then
    SET_CACHE="--cache=true --cache-repo $CI_REGISTRY_IMAGE/$TARGET/cache"
  elif [ "$USE_CACHE" = 'cache=false' ]; then
    echo 'Not using cache.'
  else
    echo 'Error. Either cache=true or cache=false must be specified for $2.'
    return 1
  fi

  kaniko_login

  /kaniko/executor \
    --cleanup \
    --context "$CI_PROJECT_DIR" \
    --dockerfile "deploy/containers/$TARGET/Dockerfile" \
    $SET_EPH \
    $SET_CACHE \
    --snapshotMode time "$@"
}

vault_install() {

  # Install vault in $1

  set -e

  URL='https://releases.hashicorp.com/vault/0.11.6/vault_0.11.6_linux_amd64.zip'

  wget -O vault.zip "$URL"
  unzip vault.zip
  mv vault $1
  rm -rf vault.zip
}

vault_login() {

  # Log in to vault.
  # Use prod credentials if branch is master
  # Use dev credentials in any other scenario

  set -e

  export VAULT_ADDR
  export VAULT_HOST
  export VAULT_PORT
  export VAULTENV_SECRETS_FILE
  export ENV
  export ENV_NAME
  export ROLE_ID
  export SECRET_ID
  export VAULT_TOKEN

  VAULT_ADDR="https://$VAULT_S3_BUCKET.com"
  VAULT_HOST="$VAULT_S3_BUCKET.com"
  VAULT_PORT='443'
  VAULTENV_SECRETS_FILE="$CI_PROJECT_DIR/env.vars"

  if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    ENV='PROD'
    ENV_NAME='production'
    ROLE_ID="$INTEGRATES_PROD_ROLE_ID"
    SECRET_ID="$INTEGRATES_PROD_SECRET_ID"
  else
    ENV='DEV'
    ENV_NAME='development'
    ROLE_ID="$INTEGRATES_DEV_ROLE_ID"
    SECRET_ID="$INTEGRATES_DEV_SECRET_ID"
  fi

  sed -i "s/env#/$ENV_NAME#/g" "$VAULTENV_SECRETS_FILE"

  VAULT_TOKEN=$(
    vault write \
    -field=token auth/approle/login \
    role_id="$ROLE_ID" \
    secret_id="$SECRET_ID"
  )

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
  BASE_URL="https://gitlab.com/fluidattacks/default/raw/$BRANCH/commitlint-configs/others"

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
