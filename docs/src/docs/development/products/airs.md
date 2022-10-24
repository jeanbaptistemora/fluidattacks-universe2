---
id: airs
title: Airs
sidebar_label: Airs
slug: /development/airs
---

Airs is the product that contains our home page,
the description of services we provide to our customers,
our blog,
security advisories,
the careers page,
and is usually the first point of contact people have with our company.

## Public Oath

1. The home page is located at:
   [fluidattacks.com](https://fluidattacks.com/).

## Architecture

1. Airs is a static site
   built with Tachyons,
   React,
   Gatsby,
   Markdown,
   and TypeScript.
1. At build time,
   we generate search indexes to leverage search functionality through Algolia.
1. Once built,
   its static content is deployed to an
   [S3 bucket on Amazon Web Services (AWS)](/development/stack/aws/s3).
1. All of the media content (images, videos, etc)
   is stored (and served from) Cloudinary.
1. The domain's registrar is [Cloudflare](/development/stack/cloudflare),
   which also proxies incoming traffic from the users
   through the Cloudflare network (CDN, Firewall, etc),
   and caches the content for some time using Page Rules.
   Before a request is returned to the user,
   a Cloudflare Worker adds HTTP security headers like the Content-Security-Policy.
1. In order to allow developers to test their changes,
   an ephemeral environment is deployed from their Git branch
   into [web.eph.fluidattacks.com/&lt;branch&gt;](https://web.eph.fluidattacks.com).
   So that they can check that everything is OK
   before opening a Merge Request on [GitLab](/development/stack/gitlab).

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Airs](./airs-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.

### Development Environment

Follow the steps
in the [Development Environment](/development/setup/environment) section of our documentation.

When prompted for an AWS role, choose `dev`,
and when prompted for a Development Environment, pick `airs`.

### Local Environment

Just run:

```sh
universe $ m . /airs/dev
```

This will launch a replica of [fluidattacks.com](https://fluidattacks.com)
on your localhost,
which you can interactively develop and test.
