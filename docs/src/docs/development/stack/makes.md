---
id: makes
title: Makes
sidebar_label: Makes
slug: /development/stack/makes
---

## Rationale

We use [Makes](https://github.com/fluidattacks/makes)
as a wrapper over Nix
in order to simplify its usage.

## Alternatives

## Usage

### Installing Makes

1. Make sure that [Nix](/development/stack/nix) is installed on your system.

1. Follow the steps at the
   [Official Makes Documentation](https://github.com/fluidattacks/makes).

### Using Makes as an End User

You can build and run the products of your choice, for example:

```bash
$ m gitlab:fluidattacks/universe@trunk /integrates/forces --help
$ m gitlab:fluidattacks/universe@trunk /melts --help
$ m gitlab:fluidattacks/universe@trunk /reviews --help
$ m gitlab:fluidattacks/universe@trunk /skims --help
```

#### Updates

You can update Makes by installing it again, but from a higher version.

In order to update the [products](/development/products) installed with Makes
no action is required on your part,
updates are automatically rolled out to your machine
with a delay of at most one day.
However,
if you want to force an update right away,
just run `$ rm -rf ~/.makes`,
or reference an specific commit instead of `@trunk`.

### Using Makes as a Developer

You would normally clone the Universe repository and run:

```sh
universe $ m .
```

### Troubleshooting

#### General considerations

- A stable internet connection is required
- A stable DNS resolver is required.
  Please consider using the following:
  - IPv4: `1.1.1.1`, `8.8.8.8`, `8.8.4.4`
  - IPv6: `2001:4860:4860::8888`, `2001:4860:4860::8844`

#### Checklist

1. If the installation failed while installing Nix,

   1. checkout the [Nix manual](https://nixos.org/manual/nix/stable/#chap-installation)
      for more detailed installation instructions, and
   1. if the problem persists,
      please let us know at help@fluidattacks.com.

1. If the installation failed while installing Makes,
   please let us know at help@fluidattacks.com.

1. If the process failed while using `$ m gitlab:xxx /yyy`,

   1. repeat the installation of Makes and try again,

   1. refresh the cache with `$ rm -rf ~/.makes` and try again, and

   1. if the problem persists,
      please let us know at help@fluidattacks.com.

## Guidelines

Please refer to the [official manual](https://github.com/fluidattacks/makes).

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
