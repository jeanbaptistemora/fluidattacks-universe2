---
id: get-dev-keys
title: Get development keys
sidebar_label: Get development keys
slug: /devs/integrates/get-dev-keys
---

Developers can use Okta to get development AWS credentials.
This is especially useful for running a local Integrates environment.

Follow these steps to generate a key pair:

1. Install `awscli` and `aws-okta-processor`:

    ```
    $ nix-env -i awscli aws-okta-processor
    $ source ~/.profile
    ```

1. Add the following function in your shell profile (`~/.bashrc`):

    ```
    function okta-login {
        eval $(aws-okta-processor authenticate --user "<user>" --pass "<password>" --organization "fluidattacks.okta.com" --role "arn:aws:iam::205810638802:role/<role>" --application "https://fluidattacks.okta.com/home/amazon_aws/0oa1ju1nmaERwnuYW357/272" --silent --duration 32400 --environment)
        export INTEGRATES_DEV_AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
        export INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
    }
    ```
    
    Replace the parameters:
    - user (email)
    - password
    - role: use `integrates-dev` or another role

1. To get the credentials execute: 
    ```
    $okta-login
    ```

1. Use the flag `--no-aws-cache` only on this cases:
   - Run as prod.
   - Present problems with `okta-login` or aws credentials.
