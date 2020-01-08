#!/bin/bash

JOB_ID=$1
LOG_FILE=$(mktemp)
LOG_LEVEL="info"

run_cron() {
    cd /usr/src/app
    source ci-scripts/helpers/sops.sh
    sops_vars production
    /usr/bin/python3 /usr/src/app/manage.py crontab run ${JOB_ID}
    return $?
} > $LOG_FILE

run_cron
test $? || LOG_LEVEL="error"
LOG_CONTENT=$(cat ${LOG_FILE} | tr '\n' '---')

PAYLOAD='{"access_token":"'"${ROLLBAR_ACCESS_TOKEN}"'","data":{"environment":"production","level":"'"${LOG_LEVEL}"'","title":"Cron job execution on '"$(hostname -f)"'","body":{"message":{"body":"'"${LOG_CONTENT}"'"}}}}';

curl -H "Content-Type: application/json" -d "${PAYLOAD}" https://api.rollbar.com/api/1/item/
