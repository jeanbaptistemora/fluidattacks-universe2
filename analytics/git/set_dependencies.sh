#!/usr/bin/env bash

set -ev

# update package list
apt-get update

# set CPython dependencies
pip3 install \
    pyyaml \
    slackclient \
    analytics/singer/tap_git \
    analytics/singer/target_redshift

# set VPNs
mkdir ~/.ssh
apt-get install -y openfortivpn

# set AWS CLI
mkdir ~/.aws
apt-get install -y awscli

echo "[default]" > ~/.aws/credentials
echo "aws_access_key_id=$(vault read -field=aws_s3_access_key secret/serves)" >> ~/.aws/credentials
echo "aws_secret_access_key=$(vault read -field=aws_s3_secret_key secret/serves)" >> ~/.aws/credentials

echo "[default]" > ~/.aws/config
echo "region=$(vault read -field=aws_s3_default_region secret/serves)" >> ~/.aws/config
echo "output=json" >> ~/.aws/config

# set Gitinspector
git clone https://github.com/ejwa/gitinspector.git
cd gitinspector
python3 setup.py install
