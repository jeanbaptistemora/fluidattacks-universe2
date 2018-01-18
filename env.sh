#!/usr/bin/env bash

{ 
	env | grep AWS_REGION 
	env | grep AWS_ACCESS_KEY_DYNAMODB
	env | grep AWS_SECRET_KEY_DYNAMODB
	env | greo FORMSTACK_TOKENS
} > "env".list