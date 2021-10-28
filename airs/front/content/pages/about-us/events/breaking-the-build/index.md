---
slug: about-us/events/breaking-the-build/
title: Breaking the Build
subtitle: Our SecDevOps Habits
:category: events
description: The conference Breaking the Build presents Fluid Attacks'
  SecDevOps habits that allow us to keep improving every day,
  and how to implement them in your company.
keywords: Fluid Attacks, SecDevOps, Habits, Breaking the Build,
  CI-CD, Conference, Pentesting, Ethical Hacking
eventspage: yes
banner: events-bg
---

## 1\. Objective

The term `SecDevOps` has grown in popularity in recent years. However,
Webinars addressing this topic tend to only focus on its benefits, or
possible use cases, ignoring people’s main motivation to attend this
kind of event.

It is fairly safe to assume that people want to also find out **how this
works** and **where to start**. Many speakers demonstrate how to perform
tests over an extremely simple environment, completely unrelatable to
our everyday tasks, and in this case, new questions emerge, such as:
**Does this work?** Or, **how can I apply this to my company?**

Based on the above, in this talk, we seek to answer the posed questions
by sharing the methodologies and work practices, or **habits**, that
allow us to implement a `SecDevOps` culture in the execution of our
projects; from the infrastructure management to the development of our
orchestration platform for vulnerability remediation: our Attack Surface
Manager.

These habits allow us not only to increase our productivity, and
generate value for our customers on a daily basis, but also to increase
the security of our production deployments. Thereby, we have been able
to reach the following average rates:

|                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <div class="imgblock"> ![Average of deployments to production in all systems](https://res.cloudinary.com/fluid-attacks/image/upload/v1620227871/airs/about-us/events/global-average_m9xxvl.webp) <div class="title"> Average of all systems, 2020/01/01 - 2020/07/15 </div> </div> | <div class="imgblock"> ![The highest average in a system](https://res.cloudinary.com/fluid-attacks/image/upload/v1620227871/airs/about-us/events/max-average_js7kyc.webp) <div class="title"> Highest average in a system, 2020/01/01 - 2020/07/15 </div> </div> |

## 2\. Content

This **seminar/workshop** aims to implement the concepts and techniques
covered in [Burn the Datacenter](../burn-the-datacenter/). Everything is
performed **live** over real infrastructure and applications, giving the
audience a look into the backstage of the process: The tools used, the
logs that allow us to identify issues, and even the source code that
defines each step for the correct deployment of our applications, always
focusing on how our infrastructure and products are updated in **real
time**.

To help understand how everything happens and demonstrate how to take
the first step to reach this configuration, we also explain all the work
habits that have allowed us to reach this point and keep improving
daily. These include topics such as:

- Source code management inside repositories, following a **monorepo**
  structure (say goodbye to multirepo)

- Keep a clean and small environment for the developers, including the
  changes to the master branch, avoiding code accumulation and
  reaching **zero inventory** (leaving `gitflow` behind)

- Generate daily value to the customers through a **micro changes**
  methodology (instead of big changes every `3` weeks or more).

- Migrate and manage all the infrastructure as versioned source code,
  turning it into **immutable infrastructure** (avoiding management
  consoles and unauthorized changes).

- Define Continuous Integration environments as source code, `pipeline
  as code`, in a way that can easily be configured and modified for
  all kinds of tests (avoiding graphical interface limitations for
  pipeline configurations).

- Avoid servers at any cost, migrating to cloud services and reaching
  a **serverless** infrastructure.

- Safe password management when deploying an application, avoiding
  sensitive information disclosure in source code and **keeping the
  secrets protected**.

- Deploy **ephemeral environments** that allow testing all the
  developed features before passing to production (reducing project
  complexity by avoiding development environments, testing, `QA`, and
  others).

- **Breaking the build** even before making a `commit` to the
  repository using `pre-commit` to check the source code.

- Perform tests over the source code and over the deployment that
  **break the build** as a result of the smallest error (instead of
  only notifying and allowing the error to keep evolving/growing):

    - Multiplatform integration

    - Unit testing

    - Coverage

    - Strict `Linters`

    - `Security Gates (SAST y DAST)`

- Extreme reduction of `build` times by using the **cache** correctly.

- Take advantage of the features presented in the version control
  client `Git`:

    - `Peer Review`

    - `Squashing`

    - `Rebasing`

    - `Rollback`

    - `Trigger builds`

- **Telemetry** accessible to developers (not logs, only available for
  infrastructure area).

Each above-mentioned point is explained while accessing `Fluid Attacks'`
systems to look at its implementation and operation. According to the
needs or interest of the participants, it is possible to focus on the
topics they deem most important.

## 3\. Experience

This **workshop** has been presented to professionals in technology and
auditing areas for companies such as:
[`Accenture`](https://www.accenture.com/co-es/new-applied-now),
[`Arus`](https://www.arus.com.co/),
[`ATH`](https://www.ath.com.co/wps/themes/html/ath/index.html),
[`Avianca`](https://www.avianca.com/co/es/),
[`Bancolombia`](https://www.grupobancolombia.com/wps/portal/personas),
[`Banitsmo`](https://www.banistmo.com/),
[`BIVA`](https://www.biva.mx/en/web/portal-biva/home),
[`Cadena`](https://www.cadena.com.co/),
[`Cidenet`](http://cidenet.com.co/),
[`Colpatria`](https://www.colpatria.com/),
[`Cognox`](http://www.cognox.co),
[`Coordiutil`](https://www.vendesfacil.com/),
[`Corona`](https://www.corona.co/) [`EAFIT`](http://www.eafit.edu.co/),
[`Evendi Digital`](https://evendidigital.com/),
[`F2X`](https://www.f2x.com.co/), [`GCO`](http://www.gco.com.co/),
[`Grupo AVAL`](https://www.grupoaval.com/wps/portal/grupo-aval/aval/),
[`Grupo Éxito`](https://www.grupoexito.com.co/es/),
[`Interbank`](https://interbank.pe/), [`Komet
Sales`](https://www.kometsales.com/), [`Pay
valida`](https://www.payvalida.com/),
[`Protección`](https://www.proteccion.com/wps/portal/proteccion/),
[`RUNT`](https://www.runt.com.co/), [`Seti`](https://seti.com.co/) and
[`Tech and Solve`](http://www.techandsolve.com/).

## 4\. Where?

The presentation can be hosted at your company’s facilities or an
external venue.

## 5\. Duration

The **workshop** has a duration of **6 hours** (it is not possible to
reduce its duration). It comprises a live demonstration of our
practices, a morning break, and a lunch break.

## 6\. When?

The **workshop** is designed to be performed from **9 A.M.** to **3
P.M.**, with a **30-minute** break at **12 P.M.** The event date must be
scheduled in agreement between the participants and `Fluid Attacks`.

## 7\. Details

1. **Investment**: The space and food for this workshop are completely
    covered by `Fluid Attacks`. The attendees must commit their time and
    cover their transportation expenses including vehicles parking costs
    in case the facility exceeds its capacity.

2. **Material**: As with all events offered by `Fluid Attacks`, the
    event material is sent to the attendees once they complete the
    [online satisfaction
    survey](https://fluidattacks.formstack.com/forms/talk).

## 8\. Audience

The **workshop** is suitable for both technical and managerial
personnel, and the satisfaction rate for both profiles is equally high.
However, if you wish to promote new changes and experimentation within
your company, it is important to include people with decision-making
power.

The **workshop** is designed for an audience of between **12 and 14**
people on the customer side, plus `4` additional participants on `Fluid
Attacks'` side.

## 9\. Speakers

- Juan Restrepo

- [Rafael Álvarez](../../people/ralvarez/)

- Daniel Salazar
