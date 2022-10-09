---
id: compute
title: Compute
sidebar_label: Compute
slug: /development/common/compute
---

Compute is the component of Common
in charge of providing out-of-band processing muscle.
It can run jobs on-demand
and on-schedule.

## Public Oath

1. There are the following AWS Batch job queues in the `us-east-1` region:

   - `clone`: Of type `c5ad.large`.
   - `small`: Of type `c5ad.large`.
   - `medium`: Of type `c5ad.xlarge`.
   - `large`: Of type `c5ad.2xlarge`.

   And:

   - They are able to run jobs,
     but for as long as an EC2 SPOT instance last
     (so design with indempotency, and retrial mechanisms in mind).
   - They can access the internet.
   - They are of x86_64-linux architecture.
   - They start running the job within a few seconds (short queue time).

## Architecture

1. A compute environment (backed by an ECS cluster)
   runs the jobs sent to their associated queue,
   and spawns as much machine instances on EC2 as necessary.
1. A Developer either:
   - Manually submits a job to a queue.
   - Defines a schedule,
     which periodically submits a job to a queue.
1. On failure, an email is sent to development@fluidattacks.com

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /compute](./compute-arch.dot.svg)
