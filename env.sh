#!/usr/bin/env bash

{
	env | grep AWS_REGION
	env | grep AWS_ACCESS_KEY_DYNAMODB
	env | grep AWS_SECRET_KEY_DYNAMODB
	env | grep SECRET_KEY_ENV
	env | grep DB_USER
	env | grep DB_PASSWD
	env | grep DB_HOST
	env | grep DB_PORT
	env | grep AWS_ACCESS_KEY
	env | grep AWS_SECRET
	env | grep MIXPANEL
	env | grep INTERCOM
	env | grep INTERCOM_SECURE_KEY_ENV
	env | grep SLACK_BOT
	env | grep GOOGLE_OAUTH2_KEY
	env | grep GOOGLE_OAUTH2_SECRET
	env | grep AZUREAD_OAUTH2_KEY
	env | grep AZUREAD_OAUTH2_SECRET
	env | grep DRIVE_AUTHORIZATION
	env | grep FORMSTACK_TOKENS
	env | grep AWS_OUTPUT
	env | grep DEBUG_ENV
} > "env".list
