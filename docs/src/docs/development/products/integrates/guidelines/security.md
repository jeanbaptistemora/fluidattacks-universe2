---
id: security
title: Security
sidebar_label: Security
slug: /development/integrates/security
---

:::note
The product described here is in constant evolution,
this document was last updated on: 2022-11-05
:::

For context on what this product does
what the main components are,
and high-level external dependencies,
see the [Integrates](/development/integrates) product page.

## Thread Model

<!--
https://owasp.org/www-community/Threat_Modeling_Process#introduction
-->

### Components

Integrates is intended to be run in the cloud on _AWS EC2_,
behind _Cloudflare_,
the _AWS ELB_,
the _AWS EKS Ingress Controller_,
and within the _AWS VPC_.
The other components that Integrates uses can be accessed over the internet,
but they require authentication,
for instance,
_AWS Backup_,
_AWS CloudWatch_,
_AWS DynamoDB_,
_AWS OpenSearch_,
_AWS S3_,
_Compute_,
and _Secrets_,
which can be accessed using _AWS IAM prod_integrates_;
and _Cloudflare_, which can be accessed using _Secrets_.

|        Identifier         |                 Description                  |
| :-----------------------: | :------------------------------------------: |
|       _Cloudflare_        |          Domain Name, Firewall, CDN          |
|         _AWS ELB_         |                Load Balancer                 |
|         _AWS EKS_         | K8s (Ingress Controller, Deployment Manager) |
|         _AWS EC2_         |          Physical Machine Instances          |
|     _AWS CloudWatch_      |                     Logs                     |
|      _AWS DynamoDB_       |                Main Database                 |
|     _AWS OpenSearch_      |                Search Engine                 |
|         _AWS S3_          |              Cloud Blob Storage              |
|         _AWS VPC_         |     Virtual Private Cloud and Networking     |
|       _AWS Backup_        |                   Backups                    |
|         _Compute_         |       Job Queues and Schedules Manager       |
|         _Secrets_         |  Credentials and secrets of other services   |
| _AWS IAM prod_integrates_ |        `prod_integrates` AWS IAM role        |

### Entry Points

Entry points define the interfaces
through which potential attackers
can interact with the application
or supply it with data.

| Identifier |                                              Description                                               |       Trust Levels       |
| :--------: | :----------------------------------------------------------------------------------------------------: | :----------------------: |
|   _API_    | The API is intended to be used by anyone, but some endpoints require an API token or an active session | Anonymous, Authenticated |
|  _Front_   |             The FrontEnd is accessible by anyone, but some views require an active session             | Anonymous, Authenticated |

### Exit Points

Exit points might prove useful when attacking Integrates.

| Identifier |              Description              |
| :--------: | :-----------------------------------: |
|   _API_    | Data and errors returned from the API |

### Assets

Something an attacker may be interested in:

|        Identifier         |                                Description                                |          Trust Levels           |
| :-----------------------: | :-----------------------------------------------------------------------: | :-----------------------------: |
|       _Cloudflare_        |                        Domain Name, Firewall, CDN                         |              Admin              |
|          _Data_           | _AWS Backup_, _AWS CloudWatch_,_AWS DynamoDB_, _AWS OpenSearch_, _AWS S3_ |      Authenticated, Admin       |
|         _Backups_         |                      Backups of the previous assets                       |              Admin              |
|         _Secrets_         |                 Credentials and secrets of other services                 |              Admin              |
| _AWS IAM prod_integrates_ |                        `prod_integrates` IAM role                         |              Admin              |
|       Availability        |                Integrates should be available all the time                | Anonymous, Authenticated, Admin |

### Trust Levels

Access rights that the application recognizes on external entities:

|  Identifier   |                               Description                               |
| :-----------: | :---------------------------------------------------------------------: |
|   Anonymous   |                        Any user on the internet                         |
| Authenticated |          Any user with either an API token or a valid session           |
|     Admin     | Some Integrates Developers or and instance of _AWS IAM prod_integrates_ |

### Data Flow

1. Both Integrates entry points (_API_ and _Front_)
   are only accessible through the _Cloudflare_ component.
1. The _Cloudflare_ component receives all the traffic from the users
   and acts as a firewall and CDN.

   It routes traffic directed to the _Front_
   to the corresponding Blob in the _AWS S3_ component,
   and routes traffic directed to the _API_
   to the Load Balancer in the _AWS ELB_ component.

1. The _AWS ELB_ component routes traffic
   to any healthy instance
   in the _AWS EC2_ component.
1. The _AWS EC2_ component routes the traffic
   to the container running the API HTTP server.
1. The API HTTP server processes the request,
   and verifies the authentication and authorization of it,
   changing the trust level to _Authenticated_ if legit,
   or keeping the trust level as Anonymous
   if the requested action does not require any access control.
   Otherwise, the request is rejected
   and a response is sent back to the user.

1. The API HTTP server
   fulfills the request by retrieving or updating the state
   in the corresponding _Data_ assets,
   which are accessed using the _Secrets_ component.

1. Now and then, some _Data_ assets
   are replicated by the _Backups_ component.
