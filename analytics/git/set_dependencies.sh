#!/usr/bin/env bash

set -ev

# update package list
apt-get update

# set CPython dependencies
pip3 install \
    pyyaml \
    urllib3 \
    progress \
    termcolor \
    slackclient \
    continuous-toolbox \
    analytics/singer/tap_git \
    analytics/singer/target_redshift

# set VPNs
mkdir -p ~/.ssh
apt-get install -y openfortivpn

# set AWS CLI
./analytics/set-aws-cli.sh

# set Gitinspector
git clone https://github.com/ejwa/gitinspector.git
cd gitinspector
python3 setup.py install
