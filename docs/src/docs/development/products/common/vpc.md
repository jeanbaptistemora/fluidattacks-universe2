---
id: vpc
title: Virtual Private Cloud (VPC)
sidebar_label: VPC
slug: /development/common/vpc
---

A Virtual Private Cloud represents a traditional network,
but on the cloud.
It allows you to launch AWS resources
(called hosts, and usually of type _EC2 instance_) on it,
and assign private/public IPv4 addresses
so that you can locate a them within the network.

A VPC is always partitioned into subnets
(a range of addresses within the whole network),
that is physically located in one availability zone.
You always deploy a resource into a subnet,
because the subnet is what represents the physical component of the VPC.
The VPC in the other hand,
is simply a logical (virtual) way to group physical resources
and locate them.

A VPC is isolated by default.
In order for traffic to go inside or outside of the VPC
you need to define a gateway,
without a gateway a VPC is effectively a sealed "box".

A VPC has one or more Route Tables
which define to which gateway the traffic
from a host or subnet goes, if any.
It is totally fine (and in some scenarios preferred)
for a host to be ignorant of things outside of the VPC.

There is also the concept of Security Groups,
which you can attach to a host
in order to specify what traffic can get into or outside of it,
from what port, protocol, and so on.

## Public Oath

1. There is a VPC called `fluid-vpc`
   with an Internet Gateway accessible at `0.0.0.0/32`,
   and subnets as described below.
   We can add more subnets after the last one,
   but the existing subnets,
   their CIDR
   and availability zone
   is constant over time.
1. There is a Security Group called `CloudFlare`
   which allows all outbound traffic from the host,
   and allows income traffic from the CloudFlare IP addresses.

## Architecture

1. We have a single VPC for the entire company,
   which is provided by this component of Common.
   The number of VPC in an AWS account is finite and low
   (5 at the moment of writing),
   so we cannot allow other products to create their own.
   On the other hand,
   it's not a trivial amount of code
   that you would want to repeat over and over.
1. We define all of the subnets here,
   because computing their CIDR (range of addresses),
   must be done precisely and conservatively (addresses are finite).
1. This VPC has an Internet Gateway
   and a Route Table
   that allows traffic from the hosts in the VPC
   to communicate with the Internet.
   However,
   remember that this is only possible
   if the Security Group associated with the resource allows it,
   and that the Internet would only be able to access the resource
   if a public address is requested for it at creation time.
1. We offer a security group called `CloudFlare`,
   which allows all outbound traffic from the host,
   and allows income traffic from the CloudFlare IP addresses.

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /vpc](./vpc-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.
