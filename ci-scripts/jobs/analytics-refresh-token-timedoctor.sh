#!/usr/bin/env bash

analytics_refresh_token_timedoctor() {

  # Sync analytics with continuous

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  aws_login

  sops_env secrets-production.yaml default \
    analytics_auth_timedoctor

  ./analytics/auth_helper.py --timedoctor-refresh
}

analytics_refresh_token_timedoctor
