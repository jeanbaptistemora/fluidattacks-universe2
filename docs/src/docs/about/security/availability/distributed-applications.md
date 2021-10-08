---
id: distributed-applications
title: Distributed Applications
sidebar_label: Distributed Applications
slug: /about/security/availability/distributed-applications
---

[Attack Surface Manager (ASM)](https://app.fluidattacks.com/)
is hosted in an application cluster
with autoscaling policies
and distributed replicas.
This ensures high availability,
as there is always one instance
ready to receive user requests
if another stops working.
Every cluster node has at least one ASM instance running in it.
Additionally,
its front side is served via a region-distributed
[CDN](https://en.wikipedia.org/wiki/Content_delivery_network)
(content delivery network),
providing maximum speed
and availability across the globe.
