---
slug: code-quality-and-security/
title: Code Quality Must Include Security
date: 2022-11-30
subtitle: Open the door to security as a quality requirement
category: philosophy
tags: cybersecurity, security-testing, software, company, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1669830093/blog/code-quality-and-security/cover_code_quality_security.webp
alt: Photo by Dima Pechurin on Unsplash
description: Discover what is usually seen as code quality, why we believe this concept should include security and some recommendations to develop high-quality code.
keywords: Code Quality And Security, Code Quality, Manual Code Review, Automated Code Review, Secure Code Review, Standards, Requirements, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/JUbjYFvCv00
---

"Code quality" and "security" concepts in software development
do not seem as closely associated
as we might believe and should be.
Code quality should be seen as a measure
that includes security within its core properties.
Security is a variable that,
in case of showing deficiency,
can affect not only the privacy of the sensitive information
but also the integrity and functionality of the product or application
and the user experience.
In this post,
we explain what is usually seen as code quality
and why we believe this concept should include security
as one of its properties or requirements.
We also give you a couple of recommendations
on how to develop high-quality code.

## What is code quality?

When we look up the word "quality" [in the dictionary](https://www.oxfordlearnersdictionaries.com/us/definition/english/quality_1?q=quality),
it is defined as "how good or bad something is."
Therefore,
when we talk about "code quality,"
we refer to a metric
to qualify how good or bad a set of software instructions is.
But how good or bad by virtue of what?
Generally,
on the basis of a variety of characteristics or attributes.
However,
as can happen,
for instance,
with the classification of human behavior from a moral perspective,
code quality is not a definitive metric
with always shared and objective parameters
and is open to discussion.
It depends on subjectivity,
on what industries and organizations define
based on their specific needs,
requirements and approaches.
Code quality,
for example,
will not necessarily be viewed in the same way
by those who build simple mobile games
and those who develop programs
that control the machinery of enormous electric companies,
both software with such distinct criticality.

Even so,
some specific ideas seem to be shared
for almost all software projects
that allow the separation of good and bad quality code.
Bad or poor-quality code may lack coherence
and consistency in handling conventions
and be full of bugs and complexity.
Good quality code,
conversely,
is usually seen as straightforward,
bug-free,
well-documented and fulfilling its intended function
for its end users.
The following are some of those key properties shared
to qualify code quality:

- **Reliability:**
  It measures how likely it is
  that the software will work without failure,
  accomplishing its purposes during a specific period.
  This property depends on the number of errors
  present in the code.

- **Robustness:**
  It measures how well the software can cope with strange user behavior
  and other conditions
  using understandable error messages.
  This property is related to the reduced susceptibility to hidden bugs
  or the introduction of new bugs.

- **Testability:**
  It measures how well the software supports the use of tests
  that can be employed to,
  for example,
  verify certain behaviors
  or detect failures in its functionality.

- **Readability:**
  It measures how legible and understandable the software code is
  not only for its original authors
  but also for those who intend to review and edit it.
  It depends on the use of comments,
  notations, indentation, documentation and simplicity,
  among other things.

- **Maintainability:**
  It measures the ease with which the software can be maintained,
  i.e., repaired, updated and improved.
  This property depends on the code's structure,
  size, consistency and complexity.

- **Portability:**
  It measures how usable the software is on different devices,
  platforms or other environments.
  In other words,
  it measures how easily it can be transferred from one to another,
  depending on the number of required modifications.

- **Reusability:**
  It measures how much the software's pieces of code or assets
  can be replicated or reused
  (even to build upon them)
  by developers in other projects or programs.

Up to this point,
what is problematic is that after roaming the web
and glancing through various sources,
we generally don't find security
or at least not explicitly suggested
among these key properties.

## What about security?

Code quality is usually associated with the code's performance
and the experience of the end users
and the developers that work on it.
However,
shouldn't code quality also be measured by its security?
On the other hand,
doesn't security also rely on what we call quality?
Almost a decade ago,
a group of researchers shared the following words
[in a study](https://resources.sei.cmu.edu/asset_files/TechnicalNote/2014_004_001_428597.pdf)
for the Software Engineering Institute:

> Many of the Common Weakness Enumerations (CWEs),
> such as the improper use of programming language constructs,
> buffer overflows,
> and failures to validate input values,
> can be associated with poor quality coding
> and development practices.
> Improving quality is a necessary condition
> for addressing some software security issues.

Poor-quality pieces of code,
even minor errors,
resulting from inadequate coding practices,
give rise to security weaknesses and vulnerabilities
that can be exploited by malicious hackers
and generate substantial negative impacts on organizations and end users.
Security thus depends on the quality of the product.
But this is a different quality
that involves not only properties such as those listed above.
In this "upgraded code quality,"
standards and practices are introduced,
which,
if not complied with,
lead us to speak of insecurity,
just as non-compliance with other requirements
could lead us to talk about,
for instance,
unreliability or low readability.
By introducing these new standards,
we have included security as a property in the previous list.
Thus,
henceforth,
in our discourse,
code security will be taken as a factor
that plays a role in determining code quality.

Security vulnerabilities in the code jeopardize
not only the valuable performance of the software
but also the privacy of sensitive data
in case they're processed there.
The non-inclusion of security in the frequently seen code quality concept
may be partly related to the latter.
In the past,
unlike nowadays,
software products that did not involve the use of sensitive data
of the organization and its users and customers
or contact with external threats
were more abundant.
At that time,
there was a more significant concern for properties
such as reliability, testability and maintainability.
Today,
however,
in our economy,
there is much more dependence on the Internet
and web and mobile applications that transfer sensitive data,
as well as a greater number of IoT devices and interconnections.
This is why it's increasingly necessary that
security also appears as a key property
in relation to code quality.

<cta-banner
  buttontxt="Read more"
  link="/solutions/secure-code-review/"
  title="Get started with Fluid Attacks' Secure Code Review solution right now"
/>

## Developing high-quality code

Pressure to go fast to production
with innovative and competitive software products.
This workload with tight deadlines is one of the common causes
of poor-quality code development.
Although someone could say that
it's becoming increasingly rare that
functionality or reliability flaws are not addressed,
it's sure that many developers are still ignoring quality standards.
This goes without saying for those standards that incorporate security.
If some professionals do not pay enough attention
to the functionality of what they build,
they will most likely pay less attention to its security.

Even worse is when those who leave standards aside
or do not promote their use
are the same leaders or chiefs of areas in the organizations,
focused mainly on requesting speed.
Currently,
code quality,
including security,
must be seen as a priority,
starting with the leaders.
The time spent on standards training,
code reviews and error fixing is often far compensated
by the costs avoided down the road.
When not adequately addressed,
code deficiencies can accumulate.
Dealing with them can then become even more complex and costly.
A high-quality code then reduces the so-called "[technical debt](https://en.wikipedia.org/wiki/Technical_debt)."

In order to develop clean or high-quality code
(including security, let's keep it in mind)
and avoid the so-called "code smells"
or poor-quality code and security vulnerabilities,
guidelines, conventions or standards are a must.
These provide uniformity,
consistency between different team members' work,
and stability in the product.
The code quality and [secure coding best practices](../secure-coding-practices/)
associated with these standards
are shared by diverse communities
and can be disseminated and taught among collaborative teams
of developers or engineers.
Individuals with different specialties,
skills and experience levels,
including often-mentioned [security champions](../secdevops-security-champions/),
can foster secure and high-quality development among their colleagues.

To guarantee that the developed product is of high quality,
it's also necessary to resort to peer or [manual code reviews](../manual-code-review/).
Developers can see these assessments
as time-consuming and tedious tasks,
even as obstacles when they should be seen as essential objectives.
When it's not developers' colleagues and leaders,
external providers can be in charge of these reviews
to identify flaws or quality deficiencies in the code
so that they can be promptly remediated.
These reviews should not be left to the final stages
of development lifecycles.
The sooner errors are detected,
the easier, faster and cheaper their remediation.
It is also advisable that
they are carried out continuously
so that they go in tandem with the constant work of developers.

Manual code reviews should be assisted by automated tools,
such as static analysis ones,
primarily because of their wide coverage and speed,
although their detection and accuracy capabilities are limited.
Thanks to these tools,
savvy reviewers can focus on identifying more complex
and sometimes more severe errors
and security issues beyond these machines' scope.
Generally speaking,
a comprehensive review,
with expert humans and automated tools,
must take into account compliance with properties
such as those outlined in this post,
along with [security requirements](https://docs.fluidattacks.com/criteria/requirements/)
such as those we've collected and currently handle at Fluid Attacks.

These reviews can also be improved
when new techniques are incorporated.
This is why at Fluid Attacks,
with our specialty in security testing,
we go beyond the [Secure Code Review](../../solutions/secure-code-review/),
which is only a part of our comprehensive [Continuous Hacking service](../../services/continuous-hacking/).
In this service,
we conduct exhaustive reviews with techniques
such as [SAST](../../product/sast/),
[SCA](../../product/sca/),
[DAST](../../product/dast/),
[manual pentesting](../../solutions/penetration-testing/)
and [reverse engineering](../../product/re/).
In addition to using our automated tools,
Continuous Hacking has as indispensable
the intervention of our ethical hackers,
who think and act as threat actors,
anticipate risks and entry points
and simulate different possible attack scenarios.
At Fluid Attacks,
we contribute from the security field
so that your code and applications are of high quality
and keep their risk exposure as low as possible.

We invite you to try our [21-day free trial](../../free-trial/)
with assessment through our automated machines
as an introduction to the comprehensive service you can receive
when you decide to become one of our customers.
[Contact us](../../contact-us/)!
