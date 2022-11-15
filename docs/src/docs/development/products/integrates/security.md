---
id: security
title: Security
sidebar_label: Security
slug: /development/products/integrates/security
---

:::note
The product described here is in constant evolution,
this document was last updated on: 2022-11-05
:::

For context on what this product does
what the main components are,
and high-level external dependencies,
see the [Integrates](/development/products/integrates) product page.

## Threat Model

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

## Threat Categorization

### Spoofing

1. An attacker may want to impersonate our users.

   Mitigation:

   - We don't store login credentials but instead use OAuth2,
     which means that the security of the login is delegated to the provider
     that the user chooses,
     or controlled by the organization the user works for.

1. An attacker may claim to be who they are not.

   Mitigation:

   - Unless a cross-site-request-forgery,
     side-channel attack,
     or a similar vulnerability exists,
     an attacker would not be able to impersonate other users.

     This is guaranteed
     because all users are given an authentication token
     after they authenticate successfully in the application,
     which contains (in encrypted form) the user's identity.

1. An Attacker may use an expired authentication token
   to gather information about the user.

   Mitigation:

   - The session token payload is encrypted.

1. An attacker may use a left-over session of a user
   to impersonate that user.

   Mitigation:

   - There is a limit after which the user's session expires.
   - No concurrent sessions are allowed
   - API tokens can be revoked.

### Tampering

1. An attacker may tamper with an authentication token
   (session token or API token).

   Mitigation:

   - Authentication tokens use signed JWT (JSON Web Tokens),
     and the signature is validated by the server before trusting its contents.

1. An attacker may submit invalid data to the API.

   Mitigation:

   - All input validation controls happen server-side.
   - The protocol we use for the API is GraphQL,
     which enforces basic types (boolean, integer, date, ...)
     and structure on the incoming requests.
   - Some fields are added special validations using regular expressions,
     and so on.
   - Communication with the Database
     is done using the appropriate libraries
     for the task,
     which handle the specific Database language (escaping, data types, etc)
     correctly.

1. Man in the Middle.

   Mitigation:

   - Only secure communication protocols are accepted by the API server.
   - The Strict-Transport-Security response header is set.

1. An attacker may tamper with the data anyway.

   Mitigation:

   - We have backups for the most important tables in the Database.

### Repudiation

1. An attacker may repudiate who they are.

   Mitigation:

   - Requests to the API require an authentication token,
     which includes the user identity
     and can only be obtained by authenticating first.
     Therefore, there is a strong claim that the bearer of the authentication token
     is the identity it claims to be.

1. An attacker may perform destructive actions anyway.

   Mitigation:

   - Logs are sent to _AWS Cloudwatch_ identifying who did what and when.
   - In many cases, the "Historic State" is stored in the Database,
     allowing retrieval of every modification the data has had over time.

### Information disclosure

1. An attacker may use data from a breach.

   Mitigation:

   - Secrets are rotated every time someone from the staff leaves the company.
   - Information is encrypted at rest.
   - Secrets are stored in the database using proper cryptography mechanisms.

1. An attacker may access the information they would normally not have access to.

   Mitigation:

   - Apart from the authentication system,
     the authorization system forbids access unless explicitly granted.

### Denial of service

1. Symmetric Denial of Service.

   Mitigation:

   - We use Cloudflare as a proxy, CDN, and firewall,
     and have configured a rate limit per IP.

1. Asymmetric Denial of Service.

   Mitigation:

   - Upon failure of some API server instances,
     Kubernetes can heal the cluster by spinning new instances.
   - Upon increased demand,
     Kubernetes can spin new instances up to a max capacity.
   - We use monitoring solutions
     to inspect in real-time
     the slow queries happening in the application,
     and proactively optimize them
     before an attacker can exploit them in practice.

### Elevation of privilege

1. An attacker may want to elevate their current role within the application.

   Mitigation:

   - The API functions in the source code
     are easy to annotate with a "decorator",
     which is a small line of code that enforces
     the authorization automatically before executing any logic.
   - The access control of every role is centralized and as-code,
     and can only be changed by changing the source code and redeploying the application,
     so it's easy to audit changes that are made to it.
   - Who has which role happens dynamically
     through being granted access by another higher-ranked role.
     Care is taken to avoid an elevation of privileges
     by computing permissions matrices,
     where it's easy to see which role can do what.
   - We practice minimum privilege where it makes sense.

### Lateral movement

1. An attacker may use their current privileges in one system
   to gain access to another system.

   Mitigation:

   - The API server has different layers of access control,
     allowing a logical division of the data by customer.

## Design Principles

### Least Privilege

Integrates has many roles
so that every identity can be granted
one with the minimum amount of permissions.

### Fail-Safe Defaults

The application denies access by default.

### Economy of Mechanism

### Complete Mediation

Authentication tokens only carry the identity of the user,
and authorization happens many times within one request
every time a function is executed.

### Open Design

- Integrates is Free and Open Source Software,
  anyone can read its source code
  and understand the internals.
- The technical and user documentation is also public.

### Separation of Privilege

Roles are per user, group, and organization,
allowing maximum segregation.

### Least Common Mechanism

Almost all storage mechanisms are layered by organization, group, or user,
and therefore locating them requires specifying this information,
which creates a logical barrier.

### Psychological Acceptability
