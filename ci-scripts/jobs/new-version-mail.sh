#!/usr/bin/env bash

new_version_mail() {

  # Send mail with new version of the repo

  set -Eeuo pipefail

  # Import functions
  . <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/sops.sh

  local SOURCE_FILE
  local ENV_NAME

  SOURCE_FILE="$(mktemp /tmp/XXXXXXXXXX)"
  ENV_NAME='production'

  aws_login "$ENV_NAME"

  sops_env "secrets-$ENV_NAME.yaml" default \
    MANDRILL_APIKEY \
    MANDRILL_EMAIL_TO

  curl -Lo \
    "$SOURCE_FILE" \
    'https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/mail.py'

  echo "send_mail('new_version', MANDRILL_EMAIL_TO,
    context={'project': PROJECT, 'project_url': '$CI_PROJECT_URL',
      'version': _get_version_date(), 'message': _get_message()},
    tags=['general'])" >> "$SOURCE_FILE"

  python3 "$SOURCE_FILE"

  rm "$SOURCE_FILE"
}

new_version_mail
