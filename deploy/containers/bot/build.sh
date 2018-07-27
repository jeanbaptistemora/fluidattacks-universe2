#!/usr/bin/env bash

# Enable debugging.
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Exit immediately if any command returns different from zero.
set -e

# Start message
echo "---### [${SERVER}] Compilando contenedor."
CI_COMMIT_REF_NAME=$1

VAULT_CA=$(cat /usr/local/share/ca-certificates/vault-ca.crt \
  | base64 | tr -d '\n')

# Build image.
cp -a deploy/containers/common deploy/containers/bot
docker build --no-cache \
  --build-arg ci_commit_ref_name="$CI_COMMIT_REF_NAME" \
  --build-arg gitlab_login="$FI_GITLAB_LOGIN" \
  --build-arg gitlab_password="$FI_GITLAB_PASSWORD" \
  --build-arg drive_authorization="$FI_DRIVE_AUTHORIZATION" \
  --build-arg drive_authorization_client="$FI_DRIVE_AUTHORIZATION_CLIENT" \
  --build-arg documentroot="$FI_DOCUMENTROOT" \
  --build-arg ssl_key="$FI_SSL_KEY" \
  --build-arg ssl_cert="$FI_SSL_CERT" \
  --build-arg vault_ca="$VAULT_CA" \
  --build-arg vault_env="$ENV_FULL" \
  -t "registry.gitlab.com/fluidsignal/integrates/bot:$CI_COMMIT_REF_NAME" \
  deploy/containers/bot/
rm -rf common
