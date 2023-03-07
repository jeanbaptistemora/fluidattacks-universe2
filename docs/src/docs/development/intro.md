---
id: intro
title: Introduction
sidebar_label: Introduction
slug: /development
---

## Who we are

We are a [cybersecurity company](https://fluidattacks.com)
whose only purpose is to make the world
a safer place.

## What we do

- We perform comprehensive security testing
  over all of your assets.
- We use cutting-edge technologies
  and heavily trained **human hackers**.
- We report vulnerabilities back to you
  as accurately and quickly as possible.

The source code of the technologies used
is versioned in the [Universe repository][universe]
and is divided across many products.
We also have a [GitHub account][github_fluidattacks]
where we publish projects
that are more oriented towards the community
and less coupled to our model of business.
However,
this documentation focuses on the Universe repository.
The projects on GitHub have separate documentation
that can be found on each of the respective projects.

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_universe&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fluidattacks_universe)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_universe&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fluidattacks_universe)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_universe&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fluidattacks_universe)
[![Code Grade](https://api.codiga.io/project/34008/score/svg)](https://www.code-inspector.com)
[![Security Scorecard](https://img.shields.io/badge/Security%20Scorecard-A-green)](https://securityscorecard.com/security-rating/fluidattacks.com?utm_medium=badge&utm_source=fluidattacks.com&utm_campaign=seal-of-trust)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/6313/badge)](https://bestpractices.coreinfrastructure.org/projects/6313)

## Our products

- [Airs](/development/airs): Home page,
  live at [fluidattacks.com](https://fluidattacks.com/).
- [Docs](/development/docs): Reference documentation,
  live at [docs.fluidattacks.com](https://docs.fluidattacks.com/).

- [Common](/development/common): Owner of critical,
  or company-wide infrastructure and resources,
  and owner of the admin account.

- [Integrates](/development/products/integrates):
  The Attack Resistance Management platform:

  - Web interface: [app.fluidattacks.com](https://app.fluidattacks.com/).
  - API: [app.fluidattacks.com/api](https://app.fluidattacks.com/api).

- [Skims](/development/skims): Security Vulnerability Scanner.
- [Forces](/development/forces): The DevSecOps agent.
- [Sorts](/development/sorts): Machine Learning assisted tool,
  that sorts the list of files in a git repository
  by the probability of it having vulnerabilities.

- [Melts](/development/melts): CLI tool that allows Fluid Attacks' security analysts
  to clone customer git repositories

- [Observes](/development/observes): Company-wide data analytics.

- [Reviews](/development/reviews): Small tool we use
  to enforce internal policies at Merge Request time.

## Our users

We have different kinds of users,
we divide them by use case:

- **End Users**:
  They don't contribute code,
  but instead just interact with our products
  by installing them on their hosts and using the product's CLI,
  or through interacting with the product's public interface
  (an API, web interface, container image, etc).

  They are usually:

  - **Security Analysts of Fluid Attacks**:
    They usually use Sorts, Melts, and the ARM (Integrates), among others.
  - **Customers of Fluid Attacks**:
    They usually use the ARM (Integrates),
    the DevSecOps container image (Forces),
    read our blog (Airs),
    and sometimes our documentation (Docs).
  - **Community users**:
    They usually use tools like Skims in its Free and Open Source plan.

- **Developers**:
  The people who contribute code at [Universe][universe]
  and are usually hired by Fluid Attacks.
  They also contribute sometimes to our [projects on GitHub][github_fluidattacks].

:::tip free trial
**Search for vulnerabilities in your apps for free
with our automated security testing!**
Start your [21-day free trial](https://app.fluidattacks.com/SignUp)
and discover the benefits of our [Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/)
[Machine Plan](https://fluidattacks.com/plans/).
If you prefer a full service
that includes the expertise of our ethical hackers,
don't hesitate to [contact us](https://fluidattacks.com/contact-us/)
for our Continuous Hacking Squad Plan.
:::

<!--  -->

[universe]: https://gitlab.com/fluidattacks/universe
[github_fluidattacks]: https://github.com/fluidattacks
