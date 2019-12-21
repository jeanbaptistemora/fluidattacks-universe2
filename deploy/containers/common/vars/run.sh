#!/usr/bin/env bash
set -e

# Initialize integrates app.

# Import functions
. <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
. ci-scripts/helpers/sops.sh

aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set region us-east-1

if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
  ENV_NAME='production'
else
  ENV_NAME='development'
fi

sops_vars "$ENV_NAME"

if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
  ./manage.py crontab add
  crontab -l >> /tmp/mycron
  crontab /tmp/mycron
  service cron restart
fi

python3 deploy/containers/common/vars/render.py "$ENV_NAME"
./manage.py collectstatic --no-input
a2ensite integrates-ssl.conf
a2ensite 000-default.conf
/etc/init.d/td-agent restart

if [[ "$ENV_NAME" = "development" ]]; then
  service redis-server restart
  java -Djava.library.path=/usr/local/lib/dynamodb-local/DynamoDBLocal_lib -jar /usr/local/lib/dynamodb-local/DynamoDBLocal.jar -sharedDb -port 8022 &
  . deploy/containers/common/vars/provision_local_db.sh
fi

/usr/sbin/apache2ctl -D FOREGROUND
