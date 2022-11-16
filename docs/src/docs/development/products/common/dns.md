---
id: dns
title: Domain Name System (DNS)
sidebar_label: DNS
slug: /development/common/dns
---

DNS is the component of Common
that provides and controls company wide domains
not managed by any other product.

## Public Oath

1. The following domains are provided:

   - `fluidattacks.com`.
   - `fluidattacks.tech`.
   - `fluidsignal.com`.
   - `fluid.la`.
   - `fluidattacks.co`.

   And all of them:

   - Have
     [Domain Name System Security Extensions (DNSSEC)](https://en.wikipedia.org/wiki/DNSSEC)
     enabled.
   - Corresponding MX records
     (for providing email service with the corresponding provider).

1. `fluidsignal.com` and `fluidattacks.co` redirect to `fluidattacks.com`.

## Architecture

1. Our DNS provider is [Cloudflare](/development/stack/cloudflare).
1. `fluidattacks.com` is the main domain,
   and the others exists just for historical reasons
   (or to provide a safe-default in case a user mistypes the main domain)
   and therefore they just redirect to the main domain.
1. All domains also point to an email provider,
   so that people can send emails using a custom domain
   instead of the email provider directly,
   for example `someone@fluidattacks.com` instead of `someone@gmail.com`.
   This is done through pointing the MX records
   to the corresponding email provider,
   most of the times Google Workspace (Gmail).
1. A few subdomains exist,
   in order to multiplex the main domain,
   like `status.fluidattacks.com`.
1. The [Cloudflare zones](/development/stack/cloudflare)
   that support it
   have [Argo](https://blog.cloudflare.com/argo/) enabled.

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /dns](./dns-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.
