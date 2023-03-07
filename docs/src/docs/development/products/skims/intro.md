---
id: intro
title: Skims
sidebar_label: Introduction
slug: /development/skims
---

Skims is a CLI application
that can be configured to analyze source code, web services,
and other attack surfaces,
and produces detailed reports
with the security vulnerabilities found.

End Users are allowed to run Skims
as a Free and Open Source vulnerability detection tool.

[Integrates](/development/products/integrates)
configures and runs Skims periodically
to find vulnerabilities
over the surface of Fluid Attacks customers
as part of the [Machine Plan](https://fluidattacks.com/plans/).

Externally the [Scanner](/machine/scanner) can be an alias of:

- Skims, when run by End Users.
- The combination of efforts
  between Skims and Integrates,
  when part of the [Machine Plan](https://fluidattacks.com/plans/).

Skims refers only to the CLI application.

## Public Oath

1. Skims can be used by End Users
   as a Free and Open Source vulnerability detection tool.
   In other words: it can be used without authentication
   or manual intervention by Fluid Attacks staff.

1. Skims has a low rate of [False Positives](https://en.wikipedia.org/wiki/Binary_classification),
   meaning that it only reports vulnerabilities that have an impact.

1. When the existence of a vulnerability cannot be deterministically decided,
   Skims will favor a False Negative over a False Positive.
   In other words,
   it will prefer failing to report a vulnerability
   that may have a real impact
   over reporting a vulnerability that may have no impact.

## Using Skims

1. Make sure you are in a Linux x86_64 system:

   ```sh
   $ uname -ms
   Linux x86_64
   ```

1. Make sure you have the following tools installed in your system:

   - [Nix](/development/stack/nix).
   - [Makes](/development/stack/makes).

1. Now you can use Skims by calling:

   ```sh
   $ m gitlab:fluidattacks/universe@trunk /skims
   ```

   Feel free to pass the --help flag
   to learn more about the things it can do for you.

   You can run the scanner with:

   ```sh
    $ m gitlab:fluidattacks/universe@trunk /skims scan /path/to/config.yaml

    ... 🚀 !!
   ```

   The configuration format is explained in the
   [Configuration guidelines](/development/skims/guidelines/configuration).

## Architecture

1. Skims is a CLI application written in Python.
1. Most of Skims' code is related to finding vulnerabilities.
   Therefore, the best way to understand how everything works
   is by reading the source code of the CLI first
   and then following the control flow.
   You'll eventually get to the different security checks
   Skims performs.

1. The vulnerability advisories used in the
   [Source Composition Analysis (SCA) component of Skims](/development/skims/guidelines/sca)
   are added, deleted, or updated, by:

   - A Scheduler in the
     [Compute component of Common](/development/common/compute),
     which fetches the information from public vulnerability databases,
     and populates the data with new information periodically.
   - Manually by a Developer.

   The vulnerability advisories used to perform the analysis are downloaded
   from a [DynamoDB table](/development/stack/aws/dynamodb/introduction)
   or a [public S3 bucket](/development/stack/aws/s3),
   depending on what privileges the user running Skims has.

   Since access to the S3 bucket is public,
   access logs are dumped for security reasons into the `common.logging` bucket
   owned by the [Users component of Common](/development/common/users).

1. Some cloud resources are owned by Skims,
   but they are either unused
   or used by Integrates
   when running Skims
   as part of the Machine plan.
   See [Issue #7886](https://gitlab.com/fluidattacks/universe/-/issues/7886),
   and [Issue #7873](https://gitlab.com/fluidattacks/universe/-/issues/7873).

1. The [OWASP Benchmark](/machine/scanner/benchmark)
   is used to measure the quality of Skims
   when analyzing certain kinds of Java applications.

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Skims](./arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.

### Development Environment

Follow the steps
in the [Development Environment](/development/setup/environment) section of our documentation.

When prompted for an AWS role, choose `dev`,
and when prompted for a Development Environment, pick `skims`.

### Local Environment

Just run:

```sh
universe $ m . /skims
```

This will build and run the Skims CLI application,
including the changes you've made to the source code.

### Local Tests

Some tests require a local instance of [Integrates](/development/products/integrates).

To deploy a local instance of integrates,
run each command in a different terminal.

```sh
universe $ m . /integrates/back
universe $ m . /dynamoDb/skims
universe $ m . /integrates/storage/dev
```

:::tip free trial
**Search for vulnerabilities in your apps for free
with our automated security testing!**
Start your [21-day free trial](https://app.fluidattacks.com/SignUp)
and discover the benefits of our [Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/)
[Machine Plan](https://fluidattacks.com/plans/).
If you prefer a full service
that includes the expertise of our ethical hackers,
don't hesitate to [contact us](https://fluidattacks.com/contact-us/)
for our Continuous Hacking Squad Plan.
:::
