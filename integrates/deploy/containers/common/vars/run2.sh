#!/usr/bin/env bash
set -e

# Initialize integrates app.

# Import functions
. integrates.sh
. common.sh

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

helper_integrates_sops_vars "$ENV_NAME"

if echo "${HOSTNAME}" | grep -q 'integrates-master'
then
  REDIS_SERVER="${REDIS_SERVER_2}"
fi

if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
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

# http://docs.gunicorn.org/en/latest/design.html#how-many-workers
# Current number of CPUs defined at deploy/production/deployment.yaml
gunicorn backend_new.app:APP \
  --bind=0.0.0.0:8080 \
  --workers=5 \
  --worker-class=uvicorn.workers.UvicornWorker \
  --timeout=120
