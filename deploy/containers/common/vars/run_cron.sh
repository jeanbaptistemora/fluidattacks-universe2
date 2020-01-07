#!/bin/bash

JOB_ID=$1

cd /usr/src/app
source ci-scripts/helpers/sops.sh
sops_vars production
/usr/bin/python3 /usr/src/app/manage.py crontab run ${JOB_ID}
