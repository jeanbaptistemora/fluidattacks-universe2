#!/usr/bin/env bash

change_keys_integrates_jwt() {

  # Change jwt token for integrates

  set -Eeuo pipefail

  # Import functions
  . infrastructure/vault-wrapper.sh
  . ci-scripts/helpers/others.sh

  vault_login

  NEW_JWT_SECRET="$(head -c 32 /dev/urandom | base64)"

  vault_update_variables integrates/development jwt_secret "$NEW_JWT_SECRET"
  vault_update_variables integrates/production jwt_secret "$NEW_JWT_SECRET"

  deploy_integrates
}

change_keys_integrates_jwt
