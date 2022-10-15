---
id: status
title: Status
sidebar_label: Status
slug: /development/common/status
---

## Public Oath

1. The status page is available at
   [status.fluidattacks.com](https://status.fluidattacks.com).

## Architecture

1. Status is a monitoring service
   powered by [Checkly](https://www.checklyhq.com).
1. We define checks over different endpoints:
   - Airs: A web-browser based check
     that verifies our home page loads,
     and contains the company name.
   - Docs: A web-browser based check
     that verifies our documentation loads,
     and contains a title.
   - ARM: A web-browser based check
     that verifies the ARM (integrates) loads,
     and contains a title.
   - API: An authenticated GraphQL query to the ARM's API (integrates),
     that verifies that the response body
     contains the expected information.
1. A dashboard is publicly accessible
   and aggregates the checks results
   and displays availability metrics over time.
1. When a check fails,
   some users receive an alert by SMS or Email.

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /status](./status-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.
