#!/usr/bin/env bash
set -e

env | egrep 'VAULT.*'  >> /etc/environment 
a2ensite integrates-ssl.conf
a2ensite 000-default.conf
/usr/src/app/manage.py makemigrations
/usr/src/app/manage.py migrate
if [ -z "${FI_VERSION}" ]; then
  /usr/src/app/manage.py crontab add
  /usr/src/app/manage.py bot
  if [ "$CI_COMMIT_REF_NAME" = "master" ]; then
    /root/vars/cron.sh
  fi
else
  /etc/init.d/td-agent restart
  /usr/sbin/apache2ctl -D FOREGROUND
fi
