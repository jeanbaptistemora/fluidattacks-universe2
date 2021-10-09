---
id: policies
title: Policies
sidebar_label: Policies
slug: /machine/web/organization/policies
---

In the [Attack Surface Manager (ASM)](https://app.fluidattacks.com),
you can set various policies
for your organization
to help you control the risks
you are willing to take
in your groups
when you decide to accept vulnerabilities.
You can access the policies section
by clicking on the Policies tab
on your organization's home page
in ASM.

![Policies Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1622586635/docs/web/organizations/policies_section_bltci8.png)

Below we explain
each of the three policies
you can set up.

## Maximum days accepted

Here you define
the maximum number of calendar days
that a finding can be temporarily accepted;
this limit can be at most 31 calendar days.
This policy affects the execution of the
[DevSecOps agent](/machine/agent)
in case you are using it,
since temporarily accepted vulnerabilities
will not be considered
at the time of breaking your build.
This means that
you have to be careful
when setting this number
to prevent some vulnerabilities remaining unresolved
for a long time,
which increases the risk
to your applications.

## Score range to be accepted

Here you determine the temporal range of severity,
according to CVSS 3.1
(values from 0.0 to 10.0),
within which
you want vulnerabilities to be accepted.
This means that
you can control the maximum risk
you are willing to take.
As you will certainly not accept some risks,
the DevSecOps agent will break your build
for the severity scores you consider relevant.
Of course,
if you choose the recommended 0.0 score,
no vulnerability can be temporarily accepted.

## Maximum times accepted

Here you define the maximum number of times
that a vulnerability can be temporarily accepted.
If,
for example,
you set this number as one
and accept a vulnerability temporarily,
after the acceptance period passes,
or you change the treatment of that vulnerability
or remediate it,
you won't be able to accept
that same vulnerability again
in the future.
This number can be any number
you deem appropriate.
