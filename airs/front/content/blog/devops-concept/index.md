---
slug: devops-concept/
title: Breaking Down DevOps
date: 2020-05-05
subtitle: The central components of DevOps definition
category: philosophy
tags: devops, software, information, web, cloud, business
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330851/blog/devops-concept/cover_gyaf3f.webp
alt: Photo by Michael Fenton on Unsplash
description: Here we introduce DevOps, a working methodology whose principles
  are communication, collaboration, automation, continuous release,
  and quick reaction.
keywords: Devops, Software, Information, Web, Cloud, Business,
  Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/y5dUcQXzJ40
---

`DevOps` is a [predominant
phenomenon](https://www.researchgate.net/publication/297573467_Towards_DevOps_in_the_Embedded_Systems_Domain_Why_is_It_so_Hard),
a [new way of
thinking](https://dl.acm.org/doi/pdf/10.1145/2962695.2962707) and
working in software engineering that is receiving a lot of attention
nowadays. The word `DevOps` a combination of the words 'Development' and
'Operations.' In **2016**, [Jabbari et
al.](https://dl.acm.org/doi/pdf/10.1145/2962695.2962707) stated that for
this concept there was no concrete or complete definition. That’s why
they decided to do a review and collect, analyze, and compare
definitions from scientific papers to consolidate one. In their
research, **49** primary studies were meeting their requirements. They
identified in those studies "the central components of `DevOps`
definition." That’s something we’ll review in this post, to improve our
understanding of that concept.

<div class="imgblock">

![Word-cloud](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330850/blog/devops-concept/cloud_q0zb4z.webp)

<div class="title">

Figure 1. Word-cloud with the common terms used for definitions of DevOps
in the studies analyzed, excluding 'Development'
and 'Operations' —taken from [Jabbari et al.
(2016)](https://dl.acm.org/doi/pdf/10.1145/2962695.2962707)

</div>

</div>

## Components of DevOps definition

As a first component (**C1**), [Jabbari and
colleagues](https://dl.acm.org/doi/pdf/10.1145/2962695.2962707) show us
the already mentioned combination of terms 'Development' (`Dev`) and
'Operations' (`Ops`). The second component (**C2**) comprehends
communication, collaboration, and teamwork between developers and
operators. In the third component (**C3**), we can see "the main goal of
`DevOps`," which is to bridge the gap between `Dev` and `Ops` teams.
From the fourth component (**C4**), it is assumed that `DevOps` is a
modern software development method that unifies other methods and tools.
The fifth component (**C5**) is where `DevOps` is seen as a paradigm of
software delivery with continuous feedback, fast response to
modifications, and automated delivery pipelines. The sixth component
(**C6**) shows the automatic "deployment process from the source code in
version control to the production environment." The seventh component
(**C7**) is related to 'continuous integration.' Finally, the eight
component (**C8**) is where `DevOps` is taken as a method where quality
assurance is essential for improving performance.

With those components identified, [Jabbari et
al.](https://dl.acm.org/doi/pdf/10.1145/2962695.2962707) give us the
following definition of `DevOps`:

> DevOps is a development methodology (C4) aimed at bringing the gap
> (C3) between Development and Operations (C1), emphasizing
> communication and collaboration (C2), continuous integration (C7),
> quality assurance (C8) and delivery (C5) with automated deployment
> (C6) utilizing a set of development practices.

Now, with this definition as a guide, we can easily delve into different
issues about `DevOps` and always know what component or part of this
methodology we are referring to.

## Exploring a bit of DevOps

So, for instance, let’s expand what is said in **C1**, **C2**, and
**C3**. As our `CTO`, Rafael Alvarez, explains in [one of his
conferences](../../about-us/events/burn-the-datacenter/), there are
typically two teams in companies where software is created and sold as a
product or as a service. A team of developers and a team of operators.
In short, the first team, with its programming knowledge, creates the
app. The second team, which manages the hardware and operating systems,
is in charge of deployment (making the app available for customer use)
and service.

Rafael explains that the development team is often asked to change the
software quickly. In contrast, the operations team is asked to ensure
that the infrastructure remains stable and changes slowly. Therefore,
the parties tend to struggle with "political noise," slowing down the
overall process. Here is where `DevOps` methodology comes into play,
bringing those two teams together. As Rafael mentions, people are no
longer grouped by task or function but by product (or service), and we
then have cross-functional teams.

<div class="imgblock">

![C4](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330850/blog/devops-concept/c4_ezfxq0.webp)

<div class="title">

Figure 2. taken from [quickmeme.com](http://www.quickmeme.com/meme/35gk6h)

</div>

</div>

Now, focused on **C4** (not the explosive), we have that `DevOps` is
related to some software development methods: 'Waterfall,' 'Agile,' and
'Lean.' Let’s extend the information about this, mostly from what
[Freddy
Yumba](https://medium.com/@freddyyumba/contrasting-the-waterfall-model-agile-lean-and-devops-a95cd9acf58)
shares.

Waterfall is a traditional linear plan-driven approach to software
development. So, it is assumed that all requirements can be specified
before starting the development process. Each phase must end before
moving on to the next. Results in detailed documents must be signed, and
these are measures of progress. In this model, the integration of later
changes may mean redesigning the entire system. So, it is said that it
doesn’t accommodate well to modifications requested by users and that it
doesn’t give rise to creativity.

Instead, Agile focuses more on collaboration "[between development
teams, business people and
customer](https://medium.com/@freddyyumba/contrasting-the-waterfall-model-agile-lean-and-devops-a95cd9acf58),"
and on creativity, and rapid response to user needs. Through this
methodology, earlier and more frequent releases are sought. Besides,
communication of the development plan is preferred through face-to-face
conversations, rather than through documentation as in Waterfall.

Finally, Lean, according to
[Yumba](https://medium.com/@freddyyumba/contrasting-the-waterfall-model-agile-lean-and-devops-a95cd9acf58),
is more oriented towards improving production system operations, project
management, and the delivery of products and services. Some people see
Lean as a way to bring agility from the project level to the
organization level. In the Lean methodology, there’s an essential aim:
the elimination of waste, anything that doesn’t add value to the
development process. Therefore, unnecessary meetings, documentation, and
tasks are discarded as much as possible.

`DevOps` arises by mixing Agile and Lean principles and practices, but
it’s more than that. As [the
author](https://medium.com/@freddyyumba/contrasting-the-waterfall-model-agile-lean-and-devops-a95cd9acf58)
says: `DevOps` is "a new culture, corporate philosophy, and way of
working." It is a result of the experiences of many people and the
desire to create and maintain organizations with high-speed,
high-performance processes and exceptional `IT` products and services.

Well, talking about more components, 'continuous integration' (**C7**)
is one of the drivers of the `DevOps` culture. We know that development
practice can be made from different machines and locations. With
'continuous integration,' we mean that the resulting code is integrated
into a shared repository over and over again during the day, even every
day. This is something different from what we were used to, years ago,
when integration was quite late.

Additionally, as part of `DevOps` methodology, an automated build
verifies each check-in, which serves to detect bugs and other problems
quickly (**C8**), without waiting for full code integration and the
deployment of the entire system. Then we have continuous, automated, and
fast delivery (**C5**), with software always ready for the production
environment, to be released to users whenever required.

In `DevOps`, there’s increased responsiveness to customer requirements
and needs. With a continuous deployment (**C6**), companies in the web
domain, as is commented by [Lwakatare and
colleagues](https://www.researchgate.net/publication/297573467_Towards_DevOps_in_the_Embedded_Systems_Domain_Why_is_It_so_Hard),
have "the opportunity to quickly verify whether their new software
features are useful to customers and \[can adopt\] practices such as
**A/B** testing." In this, "users are randomly assigned to one of the
two variants of the system for experimentation." Quick feedback becomes
quite useful to evaluate the quality of the software and continuously
repair or improve what is needed in the development process.

Today, many companies offer software as a service (`SaaS`) on the web.
"Resource virtualization and cloud computing have provided the required
building blocks"
([Spinellis, 2016](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7458759)).
`DevOps` proves to be quite useful for those companies with `SaaS`,
since from this methodology, [extensive control of the infrastructure is
achieved](https://www.researchgate.net/publication/297573467_Towards_DevOps_in_the_Embedded_Systems_Domain_Why_is_It_so_Hard),
and the software can be quickly restructured and re-released if there
are some problems.

What happens if we implement the term 'security' in this context?

We get the much mentioned `DevSecOps` concept.

And what does that term mean?

Don’t worry; surely we’ll talk about it later.
