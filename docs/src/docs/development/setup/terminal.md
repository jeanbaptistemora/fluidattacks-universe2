---
id: terminal
title: Terminal
sidebar_label: Terminal
slug: /development/setup/terminal
---

We'll configure the terminal first.
Once the terminal is configured,
all of the applications you open from it
will inherit the development environment
and credentials.

At this point you should have Nix and Makes
already installed in your system,
so we won't go into those details.

For maximum compatibility,
we suggest you use [GNU Bash](https://www.gnu.org/software/bash/)
as the command interpreter of your terminal.

Please follow the following steps:

1. Make sure you have the following tools installed in your system:

   - [Nix](/development/stack/nix)
   - [Makes](/development/stack/makes)
   - [Git](https://git-scm.com): `$ nix-env -iA nixpkgs.git`.
   - [Direnv](https://direnv.net): `$ nix-env -iA nixpkgs.direnv`.

1. Access to your `~/.bashrc`:

   ```bash
   code ~/.bashrc
   ```

1. Add the following variables to your `~/.bashrc`
   or to a file at `$universe/.envrc.config`:

   ```bash
   export OKTA_EMAIL=<username>@fluidattacks.com
   export OKTA_PASS=<your-password>
   ```

   You can optionally omit the OKTA_PASS. In that case,
   it will be asked interactively on the terminal.

1. Add the following to the end of your `~/.bashrc`:

   ```bash
   export DIRENV_WARN_TIMEOUT=1h
   source <(direnv hook bash)
   ```

1. run the changes in your `~/.bashrc`:

   ```bash
   source ~/.bashrc
   ```

Reload your terminal for changes to be loaded.

1. Clone the
   [universe repository](https://gitlab.com/fluidattacks/universe)
   into the path of your preference.

1. Change directory to the universe repository:

   ```bash
   $ cd $universe
   $
   ```

1. Pick the AWS role you want to load AWS credentials for.
   The options may change depending on your assigned permissions:

   ```bash
   Select AWS Role:
   Account: fluidsignal (205810638802)
     [ 1 ] dev
     [ 2 ] prod_airs
     [ 3 ] prod_docs
     [ 4 ] prod_integrates
     [ 5 ] prod_melts
     [ 6 ] prod_observes
     [ 7 ] prod_skims
     [ 8 ] prod_sorts
   Selection: <type a number here>
   ```

   - This prompt will be shown only if you have multiple roles assigned.
   - If you see an authentication error,
     make sure your email and password are correct.
   - If you see the following error:

     ```
     Error: Status Code: 404
     Error: Summary: Not Found: Resource not found: me (Session)
     ERROR: SAMLResponse tag was not found!
     ```

     Please remove your [AWS Okta processor](https://github.com/godaddy/aws-okta-processor)
     configuration directory by running:

     ```bash
     $ rm -rf ~/.aws-okta-processor/
     $
     ```

     And then try again.
     This error happens when
     [AWS Okta processor](https://github.com/godaddy/aws-okta-processor)
     tries to reuse a cached expired session.

1. Pick the Development environment you want to load:

   ```text
   Select the development environment you want to load:

   Once the environment has finished loading,
   please close your code editor if it is open,
   and then open it by invoking it from this terminal.

   You can reload the environment at any moment with: $ direnv allow

   1) airs       4) integratesBack    7) reviews
   2) common     5) integratesForces  8) skims
   3) docs       6) melts             9) sorts
   Selection: <type a number here>
   ```

1. AWS commands run from this terminal
   will be authenticated to AWS now.

   If you need to get the value of the secrets explicitly,
   you can echo any of the AWS variables exported,
   namely:
   _AWS_ACCESS_KEY_ID_,
   _AWS_SECRET_ACCESS_KEY_,
   _AWS_SESSION_TOKEN_, and
   _AWS_DEFAULT_REGION_.

1. (optional) Some tools are used occasionally,
   so they are not part of the development environment,
   for instance: `kubectl`, `jq`, `awscli`, among others.

   If you require any extra tools,
   you can search them [here](https://search.nixos.org/packages)
   and install them with Nix.
   If you happen to use them very frequently,
   you can add them to the development environment.
   The development environment is yours and for your benefit,
   help us take care of it.

At this point,
you can open a new terminal,
and all of the applications you open
by calling them from this terminal
will inherit the development environment
and credentials.
This works because every command
that you execute on the terminal
(like `awscli`, `kubectl`, or your code editor)
is spawned as a child process,
and environment variables like _PATH_, _AWS\_\*_, among others,
are inherited by the child process
from the parent process.

For specific last steps to have each product running in local
please refer to products section.

[aws]: https://aws.amazon.com/
