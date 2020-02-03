#!/usr/bin/env bash
set -ev

# update package list
apt-get update

# set AWS CLI
mkdir -p ~/.aws
apt-get install -y awscli

# Import functions
. <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
. toolbox/others.sh

aws_login

new_sops_env secrets-prod.yaml default \
  aws_s3_access_key \
  aws_s3_secret_key \
  aws_s3_default_region

echo "[default]" > ~/.aws/credentials
echo "aws_access_key_id=$aws_s3_access_key" >> ~/.aws/credentials
echo "aws_secret_access_key=$aws_s3_secret_key" >> ~/.aws/credentials

echo "[default]" > ~/.aws/config
echo "region=$aws_s3_default_region" >> ~/.aws/config
echo "output=json" >> ~/.aws/config
