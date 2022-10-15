---
id: melts
title: Melts
sidebar_label: Melts
slug: /development/melts
---

Melts is the product
that allows downloading the End Users (Fluid Attacks customers) code repositories
and a few other utilities
that End Users (Fluid Attacks hackers) require now and then
like checking if a group is active,
if it has Forces,
its language,
among other functions.

## Public Oath

1. Code repositories
   can be downloaded by passing:
   `drills --pull-repos`
   to Melts.

1. An Okta login and AWS credentials
   can be gotten by passing:
   `resources --login`
   to Melts.

## Using Melts

1. Make sure you have the following tools installed in your system:

   - [Nix](/development/stack/nix).
   - [Makes](/development/stack/makes).

1. Make sure you have
   [an API token](/machine/api#authentication-with-the-arm-api-token)
   from the ARM,
   and that you put its value
   in an environment variable named `INTEGRATES_API_TOKEN`.

   You can export this variable permanently
   by adding the following line at the end of your shell startup file
   (usually `~/.bashrc`):

   ```bash
   export INTEGRATES_API_TOKEN="your-integrates-api-token"
   ```

   Now close the terminal and open it again,
   or run:

   ```bash
   $ source ~/.bashrc
   ```

1. Make sure you have logged in to AWS with:

   ```bash
   $ m gitlab:fluidattacks/universe@trunk /melts resources --login
   ```

   You will be prompted
   to input your Okta credentials.

   Following this,
   depending on what roles you have access to,
   you may be prompted to
   choose a specific role to use Melts,
   the roles are self-explanatory
   so you will have no problem
   knowing which one you need.

1. Now you can use melts by calling:

   ```bash
   $ m gitlab:fluidattacks/universe@trunk /melts
   ```

   Feel free to pass the --help flag
   to learn more about the things it can do for you.

### Troubleshooting

In case you encounter
any errors while using Melts,
there are a couple of things
you can try to fix them:

- The first thing you should do
  is follow the installation instructions again.
- The next thing you can check
  is if your `INTEGRATES_API_TOKEN`
  hasn't expired,
  for this you only need to
  repeat the steps shown
  [here](/machine/api#using-the-arm-api-token)
  for updating your API token,
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
  with the appropriate credentials
  and choosing the correct role,
  if applicable,
  you should have solved any problems
  regarding permissions.
- If none of these work,
  get in contact
  with the `Fluid Attacks` team
  sending an e-mail to
  help@fluidattacks.com
  to assist you with any problems.

## Contributing

Please read the
[contributing](/development/contributing) page first.

### Development Environment

Follow the steps
in the [Development Environment](/development/setup) section of our documentation.

When prompted for an AWS role, choose `dev`,
and when prompted for a Development Environment, pick `melts`.

### Local Environment

Just run:

```sh
universe $ m . /melts
```

This will build and run the Melts CLI application,
including the changes you've made to the source code.
