#!/bin/bash

# Enable debugging.
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Exit immediately if any command returns different from zero.
set -e

# Start message
echo "---### [${SERVER}] Compilando contenedor."
CI_COMMIT_REF_NAME=$1
FI_GITLAB_LOGIN=$2
FI_GITLAB_PASSWORD=$3
FI_DRIVE_AUTHORIZATION=$4
FI_DOCUMENTROOT=$5
FI_SSL_CERT=$6
FI_SSL_KEY=$7
FI_DRIVE_AUTHORIZATION_CLIENT=$8
TORUS_TOKEN_ID=$9
TORUS_TOKEN_SECRET=$10
TORUS_ORG=$11
TORUS_PROJECT=$12

if [ "$CI_COMMIT_REF_NAME" = "master" ]; then
	export TORUS_ENVIRONMENT=production
else
	export TORUS_ENVIRONMENT=development
fi

# Build image.
cp -a ../common .
docker build --no-cache --build-arg ci_commit_ref_name="$CI_COMMIT_REF_NAME" \
	--build-arg gitlab_login="$FI_GITLAB_LOGIN" \
    --build-arg gitlab_password="$FI_GITLAB_PASSWORD" \
    --build-arg drive_authorization="$FI_DRIVE_AUTHORIZATION" \
    --build-arg documentroot="$FI_DOCUMENTROOT" \
    --build-arg ssl_cert="$FI_SSL_CERT" \
    --build-arg ssl_key="$FI_SSL_KEY" \
    --build-arg drive_authorization_client="$FI_DRIVE_AUTHORIZATION_CLIENT" \
    --build-arg torus_token_id="$TORUS_TOKEN_ID" \
    --build-arg torus_token_secret="$TORUS_TOKEN_SECRET" \
    --build-arg torus_org="$TORUS_ORG" \
    --build-arg torus_project="$TORUS_PROJECT" \
    --build-arg torus_environment="$TORUS_ENVIRONMENT" \
	-t "registry.gitlab.com/fluidsignal/integrates/bot:$CI_COMMIT_REF_NAME" .
rm -rf common
