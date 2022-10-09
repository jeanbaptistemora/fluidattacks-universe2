---
id: docs
title: Docs
sidebar_label: Docs
slug: /development/docs
---

Docs is the product that contains our documentation.

Surprising, isn't it?

## Public Oath

1. The documentation is located at:
   [docs.fluidattacks.com](https://docs.fluidattacks.com/).

## Architecture

1. Docs is a static site
   built with [Docasaurus](https://docusaurus.io/),
   [JavaScript](https://en.wikipedia.org/wiki/JavaScript),
   [Graphviz](https://graphviz.org/),
   and [Markdown](https://www.markdownguide.org/).
1. At build time,
   we generate search indexes to leverage search functionality through Algolia,
   and transform the `.dot` source files into SVG format using Graphviz.
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
   In top of this, we have a few redirections from `doc` to `docs`,
   just in case a user forgets the `s`.
1. In order to allow developers to test their changes,
   an ephemeral environment is deployed from their Git branch
   into [docs-dev.fluidattacks.com/&lt;branch&gt;](https://docs-dev.fluidattacks.com).
   So that they can check that everything is OK
   before opening a Merge Request on [GitLab](/development/stack/gitlab).

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Docs](./docs-arch.dot.svg)

<!--
Conventions for Arch:

AWS
    bgcolor="0.1 0.1 1.0"
    node[fillcolor="0.1 0.5 1.0"]
  edge[color="0.1 1.0 1.0"]
Cloudflare
    bgcolor="0.6 0.1 1.0"
    node[fillcolor="0.6 0.5 1.0"]
  edge[color="0.6 1.0 1.0"]
GitLab
    bgcolor="0.8 0.1 1.0"
    node[fillcolor="0.8 0.5 1.0"]
  edge[color="0.8 1.0 1.0"]
Other:
    bgcolor="0.0 0.0 0.95"
    node[fillcolor="0.0 0.0 0.8"]
  edge[color="0.0 0.0 0.0"]
-->
