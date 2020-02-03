#!/usr/bin/env bash

analytics_sync_git() {

  # Sync analytics with continuous

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . toolbox/others.sh

  aws_login

  new_sops_env secrets-prod.yaml default \
    analytics_gitlab_user \
    analytics_gitlab_token

  # Vault login
  curl --request POST \
       --silent \
       --data '{"role_id":"'"${SERVES_ROLE_ID}"'",
                "secret_id":"'"${SERVES_SECRET_ID}"'"}' \
    "${VAULT_ADDR}/v1/auth/approle/login" | jq -r '.auth.client_token' > ~/.vault-token

  ./analytics/git/set_dependencies.sh
  python3 analytics/git/clone_us.py 2>&1 \
    | aws s3 cp - s3://fluidanalytics/clone_us.log
  python3 analytics/git/clone_them.py 2>&1 \
    | tee clone_them.log | aws s3 cp - s3://fluidanalytics/clone_them.log
  python3 analytics/git/generate_stats.py || true
  python3 analytics/git/generate_config.py 2>&1 \
    | aws s3 cp - s3://fluidanalytics/generate_config.log
  ./analytics/git/sync_forked.sh
  ./analytics/git/taint_all.sh
  rm -fr ~/.aws
}

analytics_sync_git
