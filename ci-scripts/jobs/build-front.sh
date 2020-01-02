#!/usr/bin/env bash

build_front() {

    # Builds front

    set -e

    # import functions
    . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
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

    FI_VERSION=$(app_version)
    cp -a /npm-deps/front/node_modules front/
    npm run --prefix front/ build
    sed -i "s/integrates_version/v. $FI_VERSION/g" app/assets/dashboard/app-bundle.min.js
}

build_front
