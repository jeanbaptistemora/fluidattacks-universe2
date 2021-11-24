---
slug: secure-infra-code/
title: Secure Cloud as Code
date: 2019-05-02
category: programming
subtitle: The weakest link in security is not the technology.
tags: protect, information, business, cloud, security, flaw
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331091/blog/secure-infra-code/cover_fmeyzr.webp
alt: Lock on a fence
description: Here we want to help you secure your deployments and avoid
  common mistakes. Infrastructure as code is one of the easiest ways
  to leverage cloud computing.
keywords: Cloud, Information, Security, Protection, Hacking, Best Practices,
  Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/BJHN6Do8kjQ
---

`Amazon Web Services` ([AWS](https://aws.amazon.com/)) is one of the
biggest cloud services used by thousands of companies around the world,
and with a centralized and strong security, it is one of the best on the
market. Services like [Terraform](https://www.terraform.io/) or `AWS`
[CloudFormation](https://aws.amazon.com/cloudformation/) allow us to
write our infrastructure definitions as code in an easy and maintainable
way, being capable of storing it on a repository, deploying it using
`Continuous Integration` (`CI`) and changing the infrastructure on the
fly with minimal to no availability issues. Securing this new way of
infrastructure is a must. As a pentester, I have seen many
vulnerabilities in how the code is written, stored and deployed, which
are also mistakes that we should avoid in order to present the most
robust infrastructure. Here we are going to discuss some of the most
critical and recurrent holes in an `AWS` Infrastructure as Code (`IaC`).

Let’s talk about credentials. `AWS` provides a powerful way of storing
and managing credentials named `Identity and Access Management`
([IAM](https://aws.amazon.com/iam/)). Here we can create users and
assign roles, permissions and secret keys, one of the most important
things when we talk about `IaC`. These are a set of key pairs consisting
of an `AccesKey` and a `SecretKey` that allow us to connect to the
service using the `AWScli`, the provider of `IaC cli` or our own `CI`
pipelines.

We all know that we should protect our credentials; this is the first
thing that appears when we talk about confidentiality but, are you truly
protecting your credentials on your `IaC` environment? The answer is no.
The most common faults that we find when we test `IaC` deployments are
clear text secrets and hard-coded credentials. Even though your code is
“secure” in a password protected repository, there is no need to store
`AWS` keys on it; anyone with access to the code can view and consume
your keys, causing loss of confidentiality, integrity and availability
of the data and services that you want to protect. Even if you encrypt
your keys, you must not store them in your code. I have seen keys with a
`base64` encoding that anyone can view anyway, keys encrypted with old
algorithms that a pentester can bruteforce and keys encrypted with a
secure algorithm (like `AES`) with the decryption key hard-coded in
clear text or encoded with `base64`. So, what is the solution to this
problem? Use environment variables.

An environment variable is an easy and secure way of storing your
credentials. You can control who has access to these keys and change
them without touching your code, but you need to be sure to delete them
from your repository history or change them when you migrate to
environment variables (We can find them with tools like
[Trufflehog](https://github.com/dxa4481/truffleHog)). Services like
[Gitlab CI](https://about.gitlab.com/product/continuous-integration/)
have this method, or you can use a service for credential storage like
[AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) or
[Hashicorp Vault](https://www.vaultproject.io/) to securely store your
keys and passwords, access them whenever you need and have a clear
principle of roles and least privilege, so important when you want to
maintain confidentiality. And, talking about roles, are you setting them
correctly? Again, nope.

As I said, `AWS` has a module named `IAM` where we can set users, roles
and access keys to the `AWS` environments. Most of the times I have
compromised `AWS` keys, they were configured with excessive permissions.
Keys that should only have access to the `Amazon Simple Storage Service`
([Amazon S3](https://aws.amazon.com/s3/)) also have access to the `AWS
Secrets Manager`, `Amazon Elastic Compute Cloud`
([EC2](https://aws.amazon.com/ec2/)) and so on.

An attacker (`80%` of the time an employee) that obtains credentials as
we saw on the last point could access almost all of the organization
cloud infrastructure, extracting more secrets, reading and/or modifying
`S3` web pages and files, shutting down servers, among others. Having
the principle of least privilege on your cloud is a must, you need to
set users only for the tasks that this user is meant to do, and
configuring its roles and policies correctly.

Finally, the third and one of the most underestimated vulnerability that
I have encountered is logical access. This means access to a server
through an `SSH` port, access to an `Amazon Relational Database Service`
([RDS](https://aws.amazon.com/rds/)) through the port `3306` or `1433`,
or having the administration server open to the world using port `443`.
An open port is a window to your infrastructure increasing the attack
surface that we as pentesters can exploit, so why open it to the world?
Most of the time `IaC` developers set the network access to the services
using a `0.0.0.0` wildcard because “all” of the services should have
access, but if an attacker has access to a set of credentials for the
database, `SSH` or administration service either by brute-forcing it or
reading it in clear text (we talked about this a lot), he can wreak
havoc in your systems.

You need to set the network permissions using the principle of least
privilege too. Only the core servers should have access to the database,
only the administration network segment should have access to the
administration services and so on. This can be done by writing
restrictive network rules in your code, setting them to the specific
`IPs` that need to have access to your services, and using environment
variables in order to prevent in-office attacks when an employee changes
this settings in the code.

In conclusion, the cloud is dominating the world and `IaC` is at the
moment the best way of having your organization core accessible and
maintainable, but it comes with certain risks. You should protect your
credentials at all costs, using environmental variables or vault
services that securely store your keys. Also, have a good policy of
least privilege for your users and roles when accessing your cloud
services as well as for the network access of your servers and
databases. With this measures you can build the most robust, scalable
and maintainable infrastructure for your company and you can ensure that
it is safe against these attacks.
