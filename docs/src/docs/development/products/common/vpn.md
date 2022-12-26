---
id: vpn
title: Virtual Private Network (VPN)
sidebar_label: VPN
slug: /development/common/vpn
---

The VPN component of Common
is responsible for establishing a Site-to-Site VPN Connection
between our Network
(see the [VPC component of Common](/development/common/vpc))
and the Network of some of Fluid Attacks' customers
in order to be able to hack hosts
(web apps, servers, infrastructure, etc)
that is running inside of their Network,
and that is not accessible over the Internet for security reasons.

Understanding the basic concepts is key for understanding this component.
The following resources are highly recommended:

- [VPC component of Common](/development/common/vpc).
- <https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html>.
- <https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/what-is.html>.

## Public Oath

1. For those customers that require it,
   Site-to-Site VPN Connections are established
   between our VPC's Virtual Private Gateway,
   and their Network's Gateway Devices,
   in such a way that the hosts on the `batch_clone` subnet
   can access resources inside the customer network
   located at the address provided by the customer.
1. A client VPN endpoint exists,
   and Fluid Attacks Hackers can use it to access our VPC.

## Architecture

1. An End User (customer) has zero or more hosts
   (located at an IPv4 address),
   and optionally zero or more domain names
   (which points to an IPv4 address)
   inside of their own private network.
1. A subnet called `batch_clone`
   that is inside of Fluid Attacks Network
   will be used by our machine instances
   and we want them to be able to access the hosts
   in the End User (customer) network.
1. A Customer Gateway is setup,
   which is just a logical component
   that has the metadata of the Customer Gateway Device
   (the physical component),
   it contains values like the device's public IP,
   and serves as an abstraction over the physical device
   so that AWS knows where it is located.
1. A Site-to-Site VPN connection is setup,
   which connects the Customer Gateway Device
   with the `batch_clone` subnet.
   This connection is bidirectional,
   hosts in the `batch_clone` subnet
   are now able to see hosts in the customer network,
   and hosts in the End User (customer) network
   can see hosts in the Fluid Attacks subnet.
1. The Site-to-Site VPN has associated a few static routes
   (IPv4 addresses in the End User (customer) network)
   and they are propagated automatically
   to the main Route Table of our VPC,
   as long as at least one of the two tunnels of the Site-to-Site VPN are up.
1. For those hosts that the End User (customer)
   has defined a domain name,
   we have a Route53 Private Hosted Zone,
   in which we can associate domain names
   with IPv4 addresses,
   and a Route53 Inbound Resolver
   that resolves DNS queries originated
   from the `batch_clone` and `common` subnets
   to their value in the Route53 Private Hosted Zone.
1. In order to allow Fluid Attacks Hackers
   to access hosts in the customer network,
   we just setup a Client VPN Endpoint,
   which allows them to enter our VPC
   and use the main Route Table and the Route53 Inbound Resolvers
   so that traffic is routed as usual.

:::note
In the diagram below we depict two customers for simplicity,
but there can be many more,
and we use fake ips like `$customer_1_CIDR_1`
and fake domains like`subdomain1.customer2.com`
in order to protect their sensitive information.
:::

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /vpn](./vpn-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.
