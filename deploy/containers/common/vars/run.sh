#!/usr/bin/env bash
set -e

# Initialize integrates app.

# Import functions
. <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/sops.sh)
. ci-scripts/helpers/sops.sh

aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set region us-east-1

system_vars() {
  for var in ${@}; do
    echo "export ${var}=\"${!var}\"" >> /root/.profile
  done
}

if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
  ENV_NAME='production'
else
  ENV_NAME='development'
fi

sops_vars "$ENV_NAME"

if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    ./manage.py crontab add
    crontab -l >> /tmp/mycron
    sed -i 's|/usr/bin/python3 /usr/src/app/manage.py crontab run|/usr/src/app/deploy/containers/common/vars/run_cron.sh|g' /tmp/mycron
    crontab /tmp/mycron
    service cron restart

    system_vars \
      AWS_ACCESS_KEY_ID \
      AWS_SECRET_ACCESS_KEY \
      CI_COMMIT_REF_NAME \
      JWT_TOKEN
fi

/etc/init.d/td-agent restart

if [[ "$ENV_NAME" = "development" ]]; then
    service redis-server restart
    java -Djava.library.path=/usr/local/lib/dynamodb-local/DynamoDBLocal_lib -jar /usr/local/lib/dynamodb-local/DynamoDBLocal.jar -sharedDb -port 8022 &
    . deploy/containers/common/vars/provision_local_db.sh
fi

sleep 10

uvicorn --workers=4 \
    --host=0.0.0.0 \
    --port=80 \
    --root-path=/integrates \
    fluidintegrates.asgi:application
