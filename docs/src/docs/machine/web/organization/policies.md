---
id: policies
title: Policies
sidebar_label: Policies
slug: /machine/web/organization/policies
---

In the ASM,
it is possible to set
several policies
for your organization
to help you control
the risks you are willing to take
in your groups
when you decide to
accept vulnerabilities.
You can get to the policies section
by clicking on the **Policies** tab
that you find in the main page
of your organization.

![Policies Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1622586635/docs/web/organizations/policies_section_bltci8.png)

In the following sections
we will explain
each of the three policies
that you can set.

## Maximum days accepted

This is the maximum number
of calendar days
that a finding can be
temporally accepted,
this limit can be
at most 31 calendar days.
This policy affects
the execution of the
[DevSecOps agent](/machine/agent)
in case you are using it,
as the accepted vulnerabilities
will not be considered
at the time of
breaking your build,
which means that
you have to be careful
when setting this number
to prevent
letting some vulnerabilities
be unresolved
for much longer,
increasing the risk
for your applications.

## Score range to be accepted

This is the
temporal [CVSS 3.1](/about/glossary/#cvss)
score range
between which
a finding can be accepted,
which can be a number
between 0.0 and 10.0.
This means that
you can control
the maximum risk
that you are willing to take
based on the CVSS score
of the vulnerabilities,
as you won't be able
to accept some of them
and thus the DevSecOps agent
will break your build
for the scores
you consider relevant.
Also,
in case you choose
the recomended 0.0 score,
no vulnerabilities
will be able to be
temporally accepted.

## Maximum times accepted

This is the
maximum number of times
that a finding can be
temporally accepted.
If,
for example,
you set this number as `1`
and accept a finding temporally,
and the accepted period passes
or you change its treatment
or resolve the vulnerability,
then you won't be able
to accept that same finding again
in the future.
This number
can be anything
that you consider
appropiate.
