---
id: vpn
title: VPN
sidebar_label: VPN
slug: /development/stack/aws/vpn
---

## Rationale

[VPN][VPN] is the
[cloud-based](https://en.wikipedia.org/wiki/Cloud_computing) solution
for [Virtual private networks](https://en.wikipedia.org/wiki/Virtual_private_network)
we use.
The main reasons why we chose it
over other alternatives
are the following:

- It allows us to connect
  to our client private
  networks in a descentralized manner.
- It directly connects
  to our [AWS VPC][VPC],
  allowing other AWS services
  like [AWS Batch](/development/stack/aws/batch/)
  to reach our client private networks.
- Resources can be [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
  using [Terraform][TERRAFORM].
- It supports [AWS Client VPN](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/what-is.html),
  which allows our hackers
  to reach both our [AWS VPC][VPC]
  and client private networks
  from their local machines.
- It [supports SAML authentication](https://aws.amazon.com/blogs/networking-and-content-delivery/authenticate-aws-client-vpn-users-with-saml/)
  using [Okta](/development/stack/okta).
- It supports [DNS resolving](https://aws.amazon.com/premiumsupport/knowledge-center/client-vpn-how-dns-works-with-endpoint/)
  using [AWS Route53](https://aws.amazon.com/route53/).

## Alternatives

- **On-premise router:**
  Before using [VPN][VPN],
  we used to connect all our client
  virtual networks to our
  Medellín office router.
  Such aproach had several disadvantages,
  being lack of accesibility, scalability and reproducibility
  some of the biggest.
- **[OpenVPN Cloud](https://openvpn.net/cloud-vpn/):**
  It is a [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service)
  VPN solution.
  It didn't have a [Terraform][TERRAFORM] module,
  which impacted reproducibility and traceability.
  Overall complexity was also higher as it required
  to integrate our [AWS VPC][VPC]
  using stateful [EC2](/development/stack/aws/ec2) runners,
  plus also connecting all our client endpoints to it.

## Usage

We use [VPN][VPN] for

- Using [AWS Batch](/development/stack/aws/batch/)
  to connect to our client private networks in order to
  access their source code repositories.
- Allowing hackers to connect to our client private environments
  for executing [DAST](https://en.wikipedia.org/wiki/Dynamic_application_security_testing).
- Allowing developers to connect to our [AWS VPC][VPC]
  for debugging and development purposes.

## Guidelines

### General

- Any changes to [VPN][VPN] infrastructure
  must be done
  via [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
- To learn how to test and apply infrastructure
  via [Terraform][TERRAFORM],
  visit the [Terraform Guidelines](/development/stack/terraform#guidelines).
- Infrastructure source code
  can be found [here](https://gitlab.com/fluidattacks/product/-/tree/master/common/vpc/infra).
- All [VPN][VPN] client configurations
  can be found [here](https://gitlab.com/fluidattacks/product/-/blob/master/common/secrets/dev.yaml#L22).
  You can use [Sops](/development/stack/sops) do decrypt such values.

### Accessing the VPN

You can connect to the [VPN][VPN]
and gain access to our [AWS VPC][VPC]
and client private networks.
In order to do so, you need to:

1. Go to the [VPN Self-Service portal](https://self-service.clientvpn.amazonaws.com/endpoints/cvpn-endpoint-05b3ce2112d0a836a):
    - Log in with your [Okta](/development/stack/okta) Credentials.
    - If you do not have enough permissions, please contact help@fluidattacks.com.
1. From the portal:
    - Download the [VPN][VPN] client configuration.
    - Download and install the AWS Client VPN for your Operating System.
1. Open the AWS Client VPN and import the downloaded configuration.
1. Connect to the VPN.

[VPN]: https://aws.amazon.com/vpn/
[VPC]: /development/stack/aws/vpc/
[TERRAFORM]: /development/stack/terraform/
