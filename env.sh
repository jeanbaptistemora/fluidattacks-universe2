#!/usr/bin/env bash

{
	env | grep FI_AWS_DYNAMODB_ACCESS_KEY
	env | grep FI_AWS_DYNAMODB_SECRET_KEY
	env | grep FI_DJANGO_SECRET_KEY
	env | grep FI_DB_USER
	env | grep FI_DB_PASSWD
	env | grep FI_DB_HOST
	env | grep FI_AWS_CLOUDWATCH_ACCESS_KEY
	env | grep FI_AWS_CLOUDWATCH_SECRET_KEY
	env | grep FI_MIXPANEL_API_TOKEN
	env | grep FI_INTERCOM_APPID
	env | grep FI_INTERCOM_SECURE_KEY
	env | grep FI_SLACK_BOT_TOKEN
	env | grep FI_GOOGLE_OAUTH2_KEY
	env | grep FI_GOOGLE_OAUTH2_SECRET
	env | grep FI_AZUREAD_OAUTH2_KEY
	env | grep FI_AZUREAD_OAUTH2_SECRET
	env | grep FI_DRIVE_AUTHORIZATION
	env | grep FI_FORMSTACK_TOKENS
	env | grep FI_AWS_OUTPUT
	env | grep FI_DEBUG
	env | grep FI_ROLLBAR_ACCESS_TOKEN
	env | grep FI_GITLAB_MACHINE
	env | grep FI_GITLAB_LOGIN
	env | grep FI_GITLAB_PASSWORD
	env | grep FI_DOCUMENTROOT
	env | grep FI_ROLLBAR_ACCESS_TOKEN
	env | grep FI_ROLLBAR_ENVIRONMENT
	env | grep CI_COMMIT_SHA
	env | grep CI_COMMIT_REF_NAME
	env | grep FI_SSL_KEY
	env | grep FI_SSL_CERT
	env | grep FI_DRIVE_AUTHORIZATION_CLIENT
	env | grep FI_AWS_S3_ACCESS_KEY
	env | grep FI_AWS_S3_SECRET_KEY
} > "env".list
