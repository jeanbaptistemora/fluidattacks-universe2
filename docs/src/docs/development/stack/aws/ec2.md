---
id: ec2
title: Elastic Compute Cloud (EC2)
sidebar_label: EC2
slug: /development/stack/ec2
---

## Rationale

[AWS EC2](https://aws.amazon.com/ec2/)
is the service we use for running
[computing machines on the cloud](https://en.wikipedia.org/wiki/Cloud_computing).
It provides the required infrastructure
for services like
our
[CI](/development/stack/gitlab-ci),
[Kubernetes Cluster](/development/stack/kubernetes),
among others.

The main reasons why we chose it
over other alternatives are:

1. It seamlessly integrates with
other [AWS](https://aws.amazon.com/)
services we use like
[ECS](https://aws.amazon.com/ecs/),
[EKS](https://aws.amazon.com/eks/),
[Batch](https://aws.amazon.com/batch/),
[Elastic Load Balancing](https://aws.amazon.com/elasticloadbalancing/),
etc.
1. It provides a wide range of
[machine types](https://aws.amazon.com/ec2/instance-types/)
that goes from 2
[Vcpus](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html)
and 0.5GB of
[RAM](https://en.wikipedia.org/wiki/Random-access_memory),
to 96
[Vcpus](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html)
and 384GB of
[RAM](https://en.wikipedia.org/wiki/Random-access_memory)
machines.
Providing us with the capability of
[vertical scaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/).
1. [Machine types](https://aws.amazon.com/ec2/instance-types/)
are also divided into different specializations.
There are
[general usage](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/general-purpose-instances.html),
[compute optimized](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compute-optimized-instances.html),
[memory optimized](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compute-optimized-instances.html),
[storage optimized](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compute-optimized-instances.html)
and
[accelerated computing](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/accelerated-computing-instances.html)
machines.
By having all these
different types of machines,
we can easily select
which ones to work with
depending on the nature
of the problem we are trying to solve.
1. It supports
[Spot Instances](https://aws.amazon.com/ec2/spot/),
which are unused instances
that are available for less than the
[on-demand](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances.html)
price.
[Spot Instances](https://aws.amazon.com/ec2/spot/)
can be up to 90% cheaper
than
[on-demand](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances.html)
instances.
[Spot Instances](https://aws.amazon.com/ec2/spot/)
can can be terminated by
[AWS](https://aws.amazon.com/)
if capacity is no longer available,
making them a perfect fit
for interruptible tasks
like
[CI/CD jobs](/development/stack/gitlab-ci),
[Batch tasks](https://aws.amazon.com/batch/)
and
[horizonally-scaled applications](https://gitlab.com/fluidattacks/product/-/blob/master/makes/applications/integrates/back/deploy/prod/k8s/deployment.yaml#L7)
like our
[ASM](https://fluidattacks.com/categories/asm/).
1. It supports
[Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html),
which allows us to automatically scale up and down
the number of machines that are running our applications.
This is especially useful when combined with
our [Kubernetes Cluster](/development/stack/kubernetes)
running on
[EKS](https://aws.amazon.com/eks/),
as multiple instances of our
[ASM](https://fluidattacks.com/categories/asm/)
can be turned on and off
based on
[specific parameters](https://gitlab.com/fluidattacks/product/-/blob/master/makes/applications/integrates/back/deploy/prod/k8s/deployment.yaml#L7).
1. It supports
[advanced networking](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-networking.html)
features that allow assigning public
[ip addresses](https://en.wikipedia.org/wiki/IP_address),
having multiple
[network interfaces](https://en.wikipedia.org/wiki/Network_interface),
connecting to
[virtual private clouds](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-vpc.html),
among others.
1. It supports
[advanced security configurations](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security.html)
like
[setting security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
for specifying what ports can be accessed,
filtered by both ip ranges and
[network protocols](https://en.wikipedia.org/wiki/Lists_of_network_protocols),
[network isolation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/infrastructure-security.html),
[connecting to instances using SSH keys](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html),
among others.
1. It
[supports](https://docs.aws.amazon.com/systems-manager/latest/userguide/prereqs-operating-systems.html)
many [operating systems](https://en.wikipedia.org/wiki/Operating_system),
including
the most common
[Linux](https://en.wikipedia.org/wiki/Linux)
distributions,
[MacOS](https://en.wikipedia.org/wiki/MacOS),
[Raspbian](https://en.wikipedia.org/wiki/Raspberry_Pi_OS),
and
[Windows Server](https://en.wikipedia.org/wiki/Windows_Server).
Giving total flexibility when implementing solutions
that require a specific
[OS](https://en.wikipedia.org/wiki/Operating_system).
1. It supports
[amazon machine images](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html),
such [virtualization](https://en.wikipedia.org/wiki/Virtual_machine)
images allow us to turn on
preconfigured instances
without having to worry
about setting things up.
1. It provides a
[dynamic resource limiting](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html)
approach,
which gives us the capability of
[horizontal scaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/).
[Sending quota increase requests](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html)
is also possible.
1. Instance resources and state
can be easily monitored using
[CloudWatch](https://aws.amazon.com/cloudwatch/).
1. Instances can have
external disks by using
[EBS](https://aws.amazon.com/ebs/),
meaning that all data within an instance
persists in case it ceases to exist.

## Alternatives

1. [Google Compute Engine](https://cloud.google.com/compute):
It did not exist at the time we migrated to the cloud.
Pending to review.
1. [Azure Compute](https://azure.microsoft.com/en-us/product-categories/compute/):
It did not exist at the time we migrated to the cloud.
Pending to review.

## Usage

We use [AWS EC2](https://aws.amazon.com/ec2/) for:

1. Running
[CI](/development/stack/gitlab-ci)
workers and bastion.
1. Running
[Kubernetes Cluster](/development/stack/kubernetes)
workers and autoscaling.
1. Running
[Batch](https://aws.amazon.com/batch/) workers.
1. Running
[Okta](/development/stack/okta) RADIUS agent.
1. Running
[ERP](https://en.wikipedia.org/wiki/Enterprise_resource_planning).
1. Running
[Jumpcloud](https://jumpcloud.com/)
LDAP agents (this is currently being deprecated).

## Guidelines

1. You can access the
[AWS EC2](https://aws.amazon.com/ec2/) console
after [authenticating on AWS](/development/stack/aws#guidelines).
