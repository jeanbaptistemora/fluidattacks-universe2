---
id: ec2
title: Elastic Compute Cloud (EC2)
sidebar_label: EC2
slug: /development/stack/aws/ec2
---

## Rationale

[AWS EC2][EC2] is the service
we use for running [computing machines on the cloud](https://en.wikipedia.org/wiki/Cloud_computing).
It provides the required infrastructure
for services like our [CI][CI],
[Kubernetes Cluster][KUBERNETES],
among others.
The main reasons why we chose it
over other alternatives
are the following:

- It seamlessly integrates with other [AWS](/development/stack/aws/)
  services we use
  like [ECS](https://aws.amazon.com/ecs/),
  [EKS](/development/stack/aws/eks/),
  [Batch][BATCH],
  [Elastic Load Balancing](/development/stack/aws/elb/),
  etc.
- It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
  certifications from
  [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
  and [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
  Many of these certifications are focused
  on granting that
  the entity follows best practices
  regarding secure [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing)
  environments
  and information security.
- It provides a wide range of [machine types](https://aws.amazon.com/ec2/instance-types/)
  from 2 [Vcpus](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html)
  and 0.5 GB [RAM](https://en.wikipedia.org/wiki/Random-access_memory),
  to 224 Vcpus and 24,576 GB RAM.
  It gives us the capability of [vertical scaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/).
- Machine types are also divided into different specializations.
  There are [general-purpose](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/general-purpose-instances.html),
  [compute-optimized](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compute-optimized-instances.html),
  [memory-optimized](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/memory-optimized-instances.html),
  [storage-optimized](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/storage-optimized-instances.html)
  and [accelerated-computing](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/accelerated-computing-instances.html)
  instances.
  By having all these types of machines,
  we can easily select
  which ones to work with
  depending on the nature of the problem
  we are trying to solve.
- It supports [Spot Instances][SPOT],
  which are unused instances
  available for less than the [on-demand](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances.html)
  price.
  Spot Instances can be up to 90%
  cheaper than on-demand instances.
  Spot Instances can be terminated by [AWS](/development/stack/aws/)
  if capacity is no longer available,
  making them a perfect fit
  for interruptible tasks
  like [CI/CD jobs][CI],
  [Batch tasks][BATCH]
  and [horizontally-scaled applications](https://gitlab.com/fluidattacks/product/-/blob/56683d3cfbc2b1be3ebe8ae6dd4627b066961aa9/makes/applications/integrates/back/deploy/prod/k8s/deployment.yaml#L7)
  like our [ASM](https://fluidattacks.com/categories/asm/).
- It supports [Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html),
  which allows us to automatically scale up and down
  the number of machines running our applications.
  This is especially useful
  when combined with our Kubernetes Cluster
  running on [EKS](/development/stack/aws/eks/),
  as multiple instances of our ASM can be turned on and off
  based on [specific parameters](https://gitlab.com/fluidattacks/product/-/blob/56683d3cfbc2b1be3ebe8ae6dd4627b066961aa9/makes/applications/integrates/back/deploy/prod/k8s/deployment.yaml#L7).
- It supports [advanced networking](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-networking.html)
  features
  that allow assigning public [IP addresses](https://en.wikipedia.org/wiki/IP_address),
  having multiple [network interfaces](https://en.wikipedia.org/wiki/Network_interface),
  connecting to [virtual private clouds](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-vpc.html),
  among others.
- It supports [advanced security configurations](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security.html)
  like [setting security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
  to specify what ports can be accessed,
  filtered by both IP ranges and
  [network protocols](https://en.wikipedia.org/wiki/Lists_of_network_protocols),
  [network isolation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/infrastructure-security.html),
  [connecting to instances using SSH keys](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html),
  among others.
- It [supports](https://docs.aws.amazon.com/systems-manager/latest/userguide/prereqs-operating-systems.html)
  many [operating systems](https://en.wikipedia.org/wiki/Operating_system),
  including
  the most common [Linux](https://en.wikipedia.org/wiki/Linux)
  distributions,
  [macOS](https://en.wikipedia.org/wiki/MacOS),
  [Raspbian](https://en.wikipedia.org/wiki/Raspberry_Pi_OS)
  and [Windows Server](https://en.wikipedia.org/wiki/Windows_Server).
  It gives total flexibility when implementing solutions
  that require a specific
  [OS](https://en.wikipedia.org/wiki/Operating_system).
- It supports [amazon machine images](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html);
  such [virtualization](https://en.wikipedia.org/wiki/Virtual_machine)
  images allow us to turn on preconfigured instances
  without having to worry
  about setting things up.
- It provides a [dynamic resource limiting](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html)
  approach,
  which gives us the capability of [horizontal scaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/).
  [Sending quota increase requests](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html)
  is also possible.
- Instance resources
  and state
  can be easily monitored
  using [CloudWatch](/development/stack/aws/cloudwatch/).
- Instances can have external disks
  by using [EBS](/development/stack/aws/ebs),
  meaning that
  all data within an instance persists
  in case it ceases to exist.

## Alternatives

> **Note:**
> [Google Compute Engine](https://cloud.google.com/compute)
> and [Azure Compute](https://azure.microsoft.com/en-us/product-categories/compute/)
> are alternatives
> that did not exist at the time we migrated to the cloud.
> A review of each of them is pending.

## Usage

We use [AWS EC2][EC2] for running

- [CI][CI] workers and bastion;
- [Kubernetes Cluster][KUBERNETES] workers and autoscaling;
- [Batch][BATCH] workers;
- [Okta](/development/stack/okta) RADIUS agent;
- [ERP](https://en.wikipedia.org/wiki/Enterprise_resource_planning);
- [Jumpcloud](https://jumpcloud.com/) LDAP agents
  (this is currently being deprecated).

## Guidelines

You can access the AWS EC2 console
after [authenticating on AWS](/development/stack/aws#guidelines).

[EC2]: https://aws.amazon.com/ec2/
[CI]: /development/stack/gitlab-ci
[KUBERNETES]: /development/stack/gitlab-ci
[BATCH]: /development/stack/aws/batch/
[SPOT]: https://aws.amazon.com/ec2/spot/
