#!/usr/bin/env bash
set -e

env > /etc/environment
/etc/init.d/td-agent restart 
a2ensite integrates-ssl.conf
a2ensite 000-default.conf
/usr/src/app/manage.py makemigrations
/usr/src/app/manage.py migrate
/usr/src/app/manage.py crontab add
if [ "$CI_COMMIT_REF_NAME" = "master" ]; then
  /root/vars/cron.sh
fi
/usr/sbin/apache2ctl -D FOREGROUND