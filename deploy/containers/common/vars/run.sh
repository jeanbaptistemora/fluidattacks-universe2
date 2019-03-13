#!/usr/bin/env bash
set -e

env | egrep 'VAULT.*'  >> /etc/environment 
a2ensite integrates-ssl.conf
a2ensite 000-default.conf
/usr/src/app/manage.py makemigrations
/usr/src/app/manage.py migrate
if [ -z "${FI_VERSION}" ]; then
  /usr/src/app/manage.py crontab add
  if [ "$CI_COMMIT_REF_NAME" = "master" ]; then
    /root/cron.sh
  fi
  /usr/src/app/manage.py bot
else
  /etc/init.d/td-agent restart
  service redis-server restart
  /usr/sbin/apache2ctl -D FOREGROUND
fi
