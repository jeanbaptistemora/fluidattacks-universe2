---
id: asm
title: Attack Surface Management
sidebar_label: Attack Surface Management
slug: /app
---

Fluid Attacks ASM (Attack Surface Management)
comes with all functions you need to manage
all your applications and vulnerabilities effectively.

To access the platform go to https://integrates.fluidattacks.com.

# Login

To authenticate in the ASM,
you need a valid user in at least one of the these providers:

1. Google
1. Azure
1. Bitbucket

For enhanced security,
we do not manage users, credentials, or MFA's.
We adopt our customer's policies.

# Organizations

All customer data is consolidated in this section.
Each organization is a data bucket
where only users of that organization can access the information.

In this section, users will find:

## Analytics

Charts and indicators will help you
know what is happening with your applications.
Information presented, among others, includes the following:

- Vulnerabilities over time
- Vulnerabilities status
- Vulnerabilities treatment
- Meantime to remediate
- Top vulnerabilities

## Portfolios

In Organizations Analytics, you have the data of all your groups.
But if you want analytics for a subset, you can use portfolios
(Here we employ the same charts and indicators).

Please check the tags in the Scope section for more information.

## Stakeholders

Some users can access your organization's data,
but this permission does not guarantee access to groups or vulnerabilities,
only access to organization-level analytics and policies.

## Policies

You can use vulnerability treatments to plan remediation.
To control the correct use of them,
you can define rules that will apply to all groups in your organization.

Policies to define:

1. Maximum number of calendar days a finding can be temporarily accepted
1. Temporary CVSS 3.1 score range within which a finding can be accepted
1. Maximum number of times a finding can be temporarily accepted

## Groups

You may have multiple apps in your organization,
and you probably want to keep their vulnerabilities separate.

You can have as many groups as you want.
One group for each application or several groups for one application,
it is your choice.

In Groups section, you will find:

### Analytics

As in the case of Organization Analytics,
Group Analytics have all the information about your group.

### DevSecOps

Fluid Attacks’ ASM includes an agent that present in the CI pipelines
can break the build for open vulnerabilities.
This section shows the result of recent executions
and more information such as the following:

- Execution date
- Execution status (secure or vulnerable)
- Checked vulnerabilities
- Strictness (Tolerant/Strict)
- Type (SAST/DAST)

### Events

In the service execution, many things can and will happen.
In the events, our analysts can report any situation that affects the service.
It can be a full or partial disruption or merely a request for information.

### Consulting

Communication is essential to achieve the remediation goal.
You can post any doubt, comment, or thought
you want to share with the Fluid Attacks team
or your team in the Consulting tab.
This section works like a forum where anyone can post and reply.

### Stakeholders

You have group access control here to define who and what they can do.
When you give access to the group, there are three role options available:

- User manager
- User
- Executive

To get more information about it, check the Roles section.

### Authors

List of git users that commit code to checked repositories.

### Scope

For an ASM, you need to define the surface
that the Fluid Attacks team will check.
The following information is required to enable the testing service:

- Roots: Git repositories where you version the application’s source code.
- Environments: URLs where applications are deployed.
- Files: Any information that could help the service.
- Tags: Keywords to build portfolios and get information
  and analytics for groups that share the tag.
- Services: Active services for the group.
- Deletion: Function to safely delete all group data.

### Vulnerabilities

One of the main sections on the platforms
is where you find all the confirmed security issues of your application.

This section is divided as follows:

#### Locations

Here you find the list of all vulnerabilities with their specific locations:
File and LoC, URL and input or IP and port.

You can ask for a reattack or change the treatment
for one or many vulnerabilities as you want.

Also, you can add tags or define a qualitative risk level.

#### Reattack

When a vulnerability is remediated,
you need to request the Fluid Attacks team to reattack
it and confirm if it was indeed remediated.

You can check in the Locations table
which vulnerabilities were requested to reattack
and verify their remediation.
After verification,
the Fluid Attacks team will inform you
through the Consulting tab about the results.

#### Treatments

Risk management is an essential part of vulnerabilities management.
You can define different treatments in the Locations tab:

- **New:** The vulnerability was reported, and there is no treatment defined.
- **In progress:** The vulnerability is going to be remediated
    and has a user responsible for that remediation.
- **Temporarily accepted:** You may not resolve the vulnerability
  and decide to coexist with the risk for some time.
  The platform accepts by default a maximum of six months.
  You can control this setting in the Organization Policies section.
- **Eternally accepted:** You may not resolve the vulnerability
  and decide to coexist with the risk forever.

#### Description

In this section you can discover
all required information to understand reported vulnerabilities.

#### Severity

For the calculation of the severity of vulnerabilities,
we use the Common Vulnerability Scoring System (CVSS) version 3.1.

#### Evidence

We provide video examples and screenshots to help you
understand the context of the vulnerabilities.

#### Tracking

Here you find the history of each Vulnerability.
What has happened to the vulnerabilities since the first one was reported.
When and by whom the treatment was closed or changed.

#### Records

Some vulnerabilities can expose customer information;
for context, we share the disclosed information in this section.

#### Roles

|                     |User|Executive|User manager|
|:-------------------:|:--:|:-------:|:----------:|
|View vulnerabilities |X   |X        |X           |
|Change treatments    |X   |X        |X           |
|Approve treatments   |    |         |X           |
|Request reattack     |X   |X        |X           |
|Add tags             |X   |X        |X           |
|Add roots            |X   |X        |X           |
|Edit roots           |X   |X        |X           |
|Delete group         |    |         |X           |
|Add users            |    |         |X           |
|Edit users           |    |         |X           |
|Receive notifications|X   |         |X           |
