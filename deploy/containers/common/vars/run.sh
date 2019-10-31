#!/usr/bin/env bash
set -e

# Initialize integrates app or bot.

env | egrep 'VAULT.*'  >> /etc/environment
aws configure set aws_access_key_id ${FI_AWS_DYNAMODB_ACCESS_KEY}
aws configure set aws_secret_access_key ${FI_AWS_DYNAMODB_SECRET_KEY}
aws configure set region us-east-1

if [ "$1" = 'app' ]; then
  ./manage.py collectstatic --no-input
  a2ensite integrates-ssl.conf
  a2ensite 000-default.conf
  /etc/init.d/td-agent restart
  service redis-server restart
  java -Djava.library.path=/usr/local/lib/dynamodb-local/DynamoDBLocal_lib -jar /usr/local/lib/dynamodb-local/DynamoDBLocal.jar -sharedDb -port 8022 &

  . deploy/containers/common/vars/provision_local_db.sh

  /usr/sbin/apache2ctl -D FOREGROUND
elif [ "$1" = 'bot' ]; then
  if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    ./manage.py crontab add
    crontab -l >> /tmp/mycron
    sed -i 's|/usr/bin|vaultenv /usr/bin|g' /tmp/mycron
    crontab /tmp/mycron
    service cron start
  fi
  ./manage.py bot
else
  echo 'Only app and bot args allowed for $1'
  exit 1
fi
