---
slug: choosing-open-source/
title: Choosing Open-Source Wisely
date: 2022-01-03
subtitle: What developers should look for in open-source software
category: opinions
tags: software, devops, vulnerability, company, security-testing, risk
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1641222993/blog/choosing-open-source/cover_oss.webp
alt: Photo by MD_JERRY on Unsplash
description:  Developers need to mitigate risks when using open-source software (OSS). We share basic aspects by which developers can guide their choice of OSS.
keywords: Open Source Software, Oss, Developers, Github, Code, License, Vulnerabilities, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/v9wN8wCPLHY
---

There's an important reason
why open-source software (OSS) represents an [advantage](https://opensource.com/life/15/12/why-open-source)
for rapid development:
Developers can use code
that's already been perfected by the open-source community
without having to write their software from scratch.
Further,
OSS implementation with the cloud's offering of Software-as-a-Service
[has been identified](https://geeky.news/technology-trends-2022-a-good-year-for-open-source-and-the-cloud/)
as an important reason for OSS success.
However,
the use of OSS is an opportunity for projects to inherit vulnerabilities
already present in OSS code.
Therefore,
developers need to mitigate the risks as much as possible.
That's why they need to evaluate and choose their open-source carefully.

The question of what indicators can be used to assess OSS
has been addressed scientifically.
Researchers Yuhang Zhao and colleagues [reviewed](https://doi.org/10.1186/s42400-021-00084-8)
56 papers published between 1999 and 2020
that aimed to identify the indicators of OSS success.
The authors define success as OSS meeting users' functional needs
without causing problems such as security issues,
license misusing issues
and program crashes.
In this post,
we would like to share the five indicator categories
the authors found across the reviewed studies.
We argue that these are basic aspects
by which development teams can guide their choice of OSS.

## Code

Developers can base their choice of OSS partially on code qualities.
Three key aspects can be identified:

### Software vulnerabilities

To understand what a vulnerability is,
we offer a combination of two separate [definitions](https://niccs.cisa.gov/about-niccs/cybersecurity-glossary)
provided by the National Initiative for Cybersecurity Careers and Studies
(NICCS):

> A characteristic of location or security posture or of design,
> security procedures,
> internal controls,
> or the implementation of any of these
> that renders an organization or asset
> (such as information or an information system)
> open to exploitation by a given threat
> or susceptible to a given hazard.

Some very important things are at stake when addressing code vulnerabilities,
including the system or its application data's access control,
availability,
confidentiality,
integrity
and monitoring mechanisms.
There's always a possibility of finding vulnerabilities in any given software.
Then,
OSS choice becomes a matter of how likely a patch is to be released quickly.
The current concern surrounding [vulnerabilities in Log4j](../log4shell/)
highlights the importance of addressing these issues promptly with upgrades.

### Source risk

The risk of supply chain attacks is [quite serious](../cybersecurity-trends-2021/).
We have mentioned while discussing the [OWASP Top 10](../owasp-top-10-2021/)
that developers need to verify the integrity
in the entire software build chain.
This implies
that they need their suppliers to think about security too.
Also,
they need to ensure their software components come from trusted sources
and are digitally signed.

### Code reusability

It's important to ensure
that the code is understandable and can be modified for other uses.
The authors [say](https://doi.org/10.1186/s42400-021-00084-8)
these factors are related
to how long it takes to actually fix any vulnerabilities present.

## License

[Open-source licenses](../look-inside-oss/) allow developers to use,
modify and share software freely.
Notably,
licenses may differ in their requirements for redistribution rights.
This means
some licenses require developers to make their source code freely available,
while others don't ask for this.
Fulfilling license obligations is especially tricky
when software includes other software with incompatible licenses.
Because of this,
developers need to check license compatibility across software components.

## Popularity

The authors identify developers' liking,
admiration and support
as indicators of OSS success.
Metrics commonly used to quantify user interest for a project
are the number of downloads over its lifespan,
hit number and number of subscribers.
Further,
[one study](https://www.researchgate.net/publication/327566664)
surveyed 400 Stack Overflow users and found
that they perceive a GitHub project's *stars* to be the most useful metric
to assess its popularity.
Later in the same study,
a survey of 791 GitHub users from all over the world revealed
that they star a project to show appreciation
(e.g., because they liked the solution),
bookmark for later retrieval
or because they used or are currently using the project.

The [review](https://doi.org/10.1186/s42400-021-00084-8) suggests
that popularity has some ties to other indicators,
such as license and sponsorship.
So,
more restrictive licenses are less popular
and sponsored projects are more popular.
Other aspects linked to popularity are project status and density.
So,
projects where users participate actively in discussions
and bug reports
are preferable.
Also,
it's been [suggested](https://faculty.fuqua.duke.edu/~moorman/Marketing-Strategy-Seminar-2015/Session%2010/Grewal,%20Lilien,%20and%20Mallapragada.pdf)
that the users infer
that more connected projects are of higher quality.
By connected,
it's meant that the target project has many contributors
who also help in other projects.

## Developers

OSS success is linked to the number of developers working on the project
and role diversity.
It's helpful to understand what attracts people to become contributors.
For instance,
[one study](https://www.researchgate.net/publication/331993921)
observed 72 weeks of growth of newcomers in 450 OSS projects on GitHub.
The properties that attracted more contributors were project popularity
(number of *stars*)
and time to merge.
This shows they're interested in good practices like giving timely review,
feedback,
and closing pull requests.

Regarding contributor engagement,
[another study](https://www.researchgate.net/publication/224209733)
surveyed 233 participants and found
that their belief that they produce the intended effects
and have control over the desired outcomes
correlates with their perceived performance
in terms of quality and quantity of contribution.
Lastly,
the [review](https://doi.org/10.1186/s42400-021-00084-8) found
that social values such as altruism,
reputation and ideology
are important motivators for developers' engagement.

## Sponsorship

A final indicator refers to financial support.
In the context of OSS,
the common sponsors are enterprises and universities,
which may enhance a project's publicity and innovation capacity.
According to the [review](https://doi.org/10.1186/s42400-021-00084-8),
"sponsorship improves the ability of OSS to deal with risks
and the possibility of maintaining long-term support from developers."
However,
there could be cases in which corporate sponsors may place restrictions
on the OSS community
that could negatively impact innovation capacity.

## Time to choose!

We just talked about the five broad indicators
that developers should keep in mind when deciding for OSS.
In short,
these are some questions teams should know the answers to:

- What are the characteristics of this OSS code?

- What license obligations apply to their particular use of this OSS?

- How many users like the solution implemented by this OSS
  and/or are using it?

- How many people work on the OSS project
  and how readily do they respond to issues found?

- Is the OSS project sponsored?
  If so,
  how does sponsorship affect innovation capability?

At `Fluid Attacks`,
we aim to find all the vulnerabilities in your team's software.
Hesitate no more and [contact us](../../contact-us/)\!
