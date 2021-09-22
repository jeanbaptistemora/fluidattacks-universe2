---
id: melts
title: Melts
sidebar_label: Melts
slug: /development/melts
---

## What is Melts?

Melts is a Fluid Attacks tool
that has many functions
for consulting and managing
the resources that every group has.
These functions allows us to
download and upload
a group's repository,
securely read and edit a group's secrets,
check certain important bits of information
about a group,
e.g.,
check if the group is active,
if it has forces,
the language of the group,
the latest fingerprint for each
of the group's repositories,
among other functions.

## Using Melts

Before starting to use Melts,
first you must do two things,
set your `INTEGRATES_API_TOKEN`
and login to AWS.

### Set the INTEGRATES_API_TOKEN environment variable

This is the first thing you have to do,
without doing this you won't be able to
use Melts at all, not even to log in.
Luckily,
we already have a guide
for getting your INTEGRATES_API_TOKEN,
you can check it out
[here](/machine/api#using-the-asm-api-token).
After obtaining the token,
you must set it as an environment variable,
in order to do this,
you have to open the file `~/.bashrc`
and then add this at the end of it.

```bash
export INTEGRATES_API_TOKEN="your-integrates-api-token"
```

Replace `your-integrates-api-token`
for the api token you previously obtained
to complete this step.

### Logging into AWS

We use okta for logging into AWS
and there is a function in Melts
to do this easily,
just use the following command to login:

```bash
m gitlab:fluidattacks/product@master /melts resources --login
```

After which you will be prompted
to input your credentials,
which are the same ones you use
when logging into okta
through the web page.
Following this,
depending on what roles you have access to,
you may be prompted to
choose a specific role to use Melts,
the roles are self-explanatory
so you will have no problem
knowing which one you need.

There is also another way
of logging into AWS,
which is more familiar for developers,
you only need to follow the steps
described in this
[guide](/development/stack/aws#get-development-keys)
but instead of using the `integrates-dev` role
you should use the `continuous-admin` role
which will allow you to use the functionalities
with admin privileges,
useful for developer purposes.

## Creating secrets as a resourcer

By using the login function
that Melts provides,
resourcers can access a role
with enough privileges
to create a project's configuration files,
specifically,
those that contain said project's secrets.
The following are the steps
needed to create these files:

- The first thing to do
  is add a function
  that we will call `switch_aws`
  to your `~/.bashrc` file,
  something you only need to do once.

  ```bash
  function switch_aws(){
    project="$1"
    local key=$(aws configure get aws_access_key_id --profile ${project})
    local secret=$(aws configure get aws_secret_access_key --profile ${project})
    local token=$(aws configure get aws_session_token --profile ${project})
    export AWS_ACCESS_KEY_ID=$key
    export AWS_SECRET_ACCESS_KEY=$secret
    export AWS_SESSION_TOKEN=$token
    aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
    aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
    aws configure set aws_session_token "$AWS_SESSION_TOKEN"
  }
  ```

- Go into your local `services` repository folder
  and then use the following command
  that uses Melts
  to log in with the admin role:

  ```bash
  m gitlab:fluidattacks/product@master /melts resources --login admin
  ```

  Enter your credentials
  when asked for them
  and then use these two commands
  in succession:

  ```bash
  aws sts get-caller-identity --profile continuous-admin
  switch_aws continuous-admin
  ```

  These allow you to
  get the necessary AWS credentials.
- After this is done
  you need to open
  the file `~/.aws/credentials`
  with your favorite editor.
- This file will have
  two sets of credentials,
  one under `continuous-admin`
  and another one under `default`,
  you need to copy
  all the information of `continuous-admin`
  and paste it under `default`
  replacing what `default` already has.
  This step is necessary
  in case the file has been modified
  while you utilize
  other Melts functions
  that interact with it.
- After that's done,
  go to the config folder
  of the group you want
  to create a secrets file for
  (`services/groups/{group}/config`)
  and create a dummy yaml file
  with a single line containing
  this: `{}`
- Then open a terminal
  in the folder
  and run this command:

  ```bash
  sops -e --kms arn:aws:kms:us-east-1:{account_id}:alias/continuous-{group} dummy.yaml > secrets-dev.yaml
  ```

  With this you will create
  the group's secrets-dev file.
- Creating the secrets-prod file
  requires a little more customization
  so you need to
  talk to the group's PM
  to create it.

## Troubleshooting

In case you encounter
any errors while using Melts,
there are a couple of things
you can try to fix them:

- The first thing you should do
  is to follow the installation instructions again.
- The next thing you can check
  is if your `INTEGRATES_API_TOKEN`
  hasn't expired,
  for this you only need to
  repeat the steps shown
  [here](/machine/api#using-the-asm-api-token)
  for updating your api token,
  and be aware of when
  it will expire next.
- Another thing that
  may be causing issues
  is a conflict in your environment variables
  that are taken when you log into AWS,
  so you can try deleting this information
  and logging in again.
  In order to do this
  use the command `rm -rf ~/.aws/credentials`
  before logging in,
  if that doesn't work
  then use `rm -rf ~/.okta*` as well.
  After doing this and logging in
  with the appropiate credentials
  and choosing the correct role,
  if applicable,
  you should have solved any problems
  regarding permissions.
- If none of these work,
  get in contact
  with the fluid attacks team
  sending an e-mail to
  help@fluidattacks.com
  to assist you with any problems.
