#!/usr/bin/env bash

analytics_refresh_token_timedoctor() {

  # Sync analytics with continuous

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . toolbox/others.sh

  aws_login

  new_sops_env secrets-prod.yaml default \
    analytics_auth_timedoctor

  ./analytics/auth_helper.py --timedoctor-refresh
}

analytics_refresh_token_timedoctor
