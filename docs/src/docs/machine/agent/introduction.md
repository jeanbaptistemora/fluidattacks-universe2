---
id: introduction
title: DevSecOps Agent
sidebar_label: Introduction
slug: /machine/agent
---

We have a component called the
**DevSecOps agent**, which is an
essential element for implementing
DevSecOps in projects.
The agent is included in CI/CD (Continuous
Integration/Continuous Deployment)
environments as a security gate, preventing
vulnerable code from reaching production.
Any change to the Target of Evaluation is
continuously verified.
The agent verifies the status of
vulnerabilities and breaks the build to
force the remediation of those that are
open and unaccepted.

In the [Policies section](/machine/web/organization/policies)
on the ASM, you can select and configure
the conditions or policies that the agent
must validate for breaking the build.
