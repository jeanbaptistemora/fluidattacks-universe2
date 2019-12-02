#!/usr/bin/env bash

change_keys_formstack() {

  # Regenerate formstack tokens for integrates

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh
  . ci-scripts/helpers/others.sh

  vault_login

  local FORMSTACK_TOKENS

  aws_login

  sops_env secrets-production.yaml default \
    FORMSTACK_EMAIL \
    FORMSTACK_PASS

  FORMSTACK_TOKENS="$(./ci-scripts/helpers/rotate_fs_keys.py)"

  vault_update_variables integrates/development
    formstack_tokens "$FORMSTACK_TOKENS"
  vault_update_variables integrates/production
    formstack_tokens "$FORMSTACK_TOKENS"

  python3 ci-scripts/helpers/rotate_fs_keys.py delete

  deploy_integrates
}

change_keys_formstack
