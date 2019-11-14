#!/usr/bin/env bash

run_wire_gitlab_bot_service() {

  # Run wire-gitla-bot service inside container

  set -Eeuo pipefail

  local TMP_FILE

  TMP_FILE="$(mktemp /tmp/XXXXXXXXXX)"

  envsubst < /etc/gitlab/gitlab.yaml > "$TMP_FILE"
  mv "$TMP_FILE" /etc/gitlab/gitlab.yaml

  java -jar gitlab.jar server /etc/gitlab/gitlab.yaml
}
