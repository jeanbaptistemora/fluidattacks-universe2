#!/bin/bash

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
JOB_ID=$1
source /root/.profile

run_cron() {
    cd /usr/src/app
    source ci-scripts/helpers/sops.sh
    sops_vars production
    /usr/bin/python3 /usr/src/app/manage.py crontab run ${JOB_ID}

    if [ $? ]; then
        LOG_LEVEL="info"
        LOG_CONTENT="Cron job ${JOB_ID} ran successfully"
    else
        LOG_LEVEL="error"
        LOG_CONTENT="Error running cron job ${JOB_ID}"
    fi
    PAYLOAD='{"access_token":"'"${ROLLBAR_ACCESS_TOKEN}"'","data":{"environment":"production","level":"'"${LOG_LEVEL}"'","title":"Cron job execution on '"$(hostname -f)"'","body":{"message":{"body":"'"${LOG_CONTENT}"'"}}}}'
    curl -H "Content-Type: application/json" -d "${PAYLOAD}" https://api.rollbar.com/api/1/item/
}

run_cron