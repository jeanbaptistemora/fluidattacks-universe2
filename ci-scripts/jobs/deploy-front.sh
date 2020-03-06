#!/usr/bin/env bash

deploy_front() {

    # Deploys front

    set -e

    # import functions
    . <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/sops.sh)
    . ci-scripts/helpers/others.sh
    . ci-scripts/helpers/sops.sh

    # Set necessary env vars
    local ENV_NAME

    if [ "$CI_COMMIT_REF_NAME" == 'master' ]; then
        ENV_NAME="production"
    else
        ENV_NAME="development"
    fi

    aws_login "$ENV_NAME"
    sops_vars "$ENV_NAME"

    ./manage.py collectstatic --no-input
}

deploy_front
