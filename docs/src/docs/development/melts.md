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

## Installing Melts

There are two main ways
of installing Melts:

### For analysts

If you are an analyst
then surely you will need melts
for your daily activities,
the main way for analysts
to install Melts
is using the `install.sh` file
present in the `services` repository.
You only need to enter the root
of the `services` repository,
and then use this command:

```bash
./install.sh
```

This command will install for you
not only Melts,
but also Sorts and Skims,
which may be of use to you as well.

### For developers

There is also a way to install
the latest version of Melts by itself
in case you don't use the `services` repository
and don't need the other two tools,
the command is the following:

```bash
curl -L fluidattacks.com/install/melts | sh
```

In case you are a developer
you may want to use Melts
to test the changes you made to it,
in this case you can simply
get into your local `product` repository
and run Melts normally,
for example, like this:

```bash
./m melts --help
```

And this will run
your local version of Melts.
However,
there are cases in which
you need to run your local Melts
from inside your local `services` repository,
in these cases you can use the following command:

```bash
nix-env -i melts -f . --option narinfo-cache-negative-ttl 1
--option narinfo-cache-positive-ttl 1
--option restrict-eval false
--option sandbox false
--option substituters 'https://fluidattacks.cachix.org https://cache.nixos.org'
--option trusted-public-keys '
    fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=
    cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=
  '
```

This will install Melts
using your local `product` repository,
and will have the changes
you have made to it.

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
melts resources --login
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