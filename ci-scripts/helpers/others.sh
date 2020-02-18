#!/usr/bin/env bash

aws_login() {
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    AWS_ACCESS_KEY_ID="$PROD_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY="$PROD_AWS_SECRET_ACCESS_KEY"
  else
    AWS_ACCESS_KEY_ID="$DEV_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY="$DEV_AWS_SECRET_ACCESS_KEY"
  fi
}

terraform_login() {
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

  aws_login

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_ACCESS_KEY"
}
