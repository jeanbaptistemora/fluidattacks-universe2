#!/usr/bin/env bash

new_version_mail() {

  # Send mail with new version of the repo

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . toolbox/others.sh

  local SOURCE_FILE

  SOURCE_FILE="$(mktemp /tmp/XXXXXXXXXX)"

  aws_login

  sops_env secrets-prod.yaml default \
    MANDRILL_APIKEY \
    MANDRILL_EMAIL_TO

  curl -Lo \
    "$SOURCE_FILE" \
    'https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/mail.py'

  echo "send_mail('new_version', MANDRILL_EMAIL_TO,
    context={'project': PROJECT, 'project_url': '$CI_PROJECT_URL',
      'version': _get_version_date(), 'message': _get_message()},
    tags=['general'])" >> "$SOURCE_FILE"

  python3 "$SOURCE_FILE"
}

new_version_mail
