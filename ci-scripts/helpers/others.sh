#!/usr/bin/env sh

kaniko_build() {

  # This script builds a Dockerfile using kaniko with cache
  # and pushes to the registry if the branch is master.
  # kaniko parameters can be added if needed.
  # Example: kaniko_build mobile --build-arg VERSION='1.2'

  set -e

  TARGET="$1"
  shift 1

  echo "{\"auths\":{\"$CI_REGISTRY\":{\"username\":\"$CI_REGISTRY_USER\",\
    \"password\":\"$CI_REGISTRY_PASSWORD\"}}}" > /kaniko/.docker/config.json

  if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    PUSH_POLICY="--destination $CI_REGISTRY_IMAGE:$TARGET"
  else
    PUSH_POLICY='--no-push'
  fi

  /kaniko/executor \
    --cleanup \
    --context "$CI_PROJECT_DIR" \
    --dockerfile "deploy/containers/$TARGET/Dockerfile" \
    $PUSH_POLICY \
    --cache=true \
    --cache-repo "$CI_REGISTRY_IMAGE/cache/$TARGET" \
    --snapshotMode time "$@"
}

vault_login() {

  # Logs in to vault.
  # Uses prod credentials if branch is master
  # Uses dev credentials in any other scenario

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

  # Gets the current version for a mobile deployment

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

  #This scripts download commitlint's configuration files

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
