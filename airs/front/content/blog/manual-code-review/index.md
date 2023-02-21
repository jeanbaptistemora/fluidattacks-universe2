---
slug: manual-code-review/
title: Indispensable Manual Code Review
date: 2022-11-25
subtitle: Use of automated tools only? Don't stick to your guns!
category: philosophy
tags: cybersecurity, security-testing, software, company, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1669424410/blog/manual-code-review/cover_manual_code_review.webp
alt: Photo by Museums Victoria on Unsplash
description: In this blog post, we present some differences between automated and manual code reviews and emphasize the latter and the procedures performed by the reviewers.
keywords: Manual Code Review, Automated Code Review, Secure Code Review, Business Logic, Standards, Requirements, Vulnerabilities, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/WGeO6dW5GZM
---

When we strive to create products in our daily work,
whatever our area,
it's time after time quite beneficial that
before delivering them,
prior to their presentation to the end users,
they're reviewed by someone else.
Receiving feedback from colleagues or leaders will not cease
to help improve our performance
and the quality of our products.
This certainly applies to software development.
Reviewing the code that developers build to shape,
for instance,
web or mobile applications,
is a fundamental process to guarantee its high quality and security.
In this post,
we compare automated and manual code reviews
and give special attention to the manual method.

## What is code review?

Code review is a process
through which a source code is systematically assessed
to verify its compliance with specific standards.
Such compliance allows the software product to remain
with a reduced amount of bugs or flaws
(it'll be free of them once in a blue moon)
that are many times the result of a slapdash approach by developers.
Code review can focus on the software's architecture,
functionality and style,
but it can also deal with its security.
Hence the term secure code review.
(Take as implicit the fact that,
when here we talk merely about "code review,"
we refer to the analysis that involves security
because a review without considering it
ends up being insufficient).

Code review is based on coding standards and requirements that,
in fact,
are what developers should bear in mind from the outset.
Errors arising from non-compliance,
no matter how small,
can take a heavy toll on the organization owning the code
and related individuals and entities,
especially when criminals exploit them.
Today,
mainly within the [DevSecOps approach](../devsecops-concept/),
it's recommended that code review be carried out early
in the software development cycle (SDLC)
before deploying the software into production.
The idea is to make this a constant operation
so that issues are reported to developers asap
and to avoid high costs in the future.

## Automated vs. manual code review

Both savvy humans and automated tools can perform code reviews.
Currently,
there's a whole raft of tools for code review.
And although these may vary in their features,
such as ease of use,
appearance and capabilities,
here we make a comparison in general terms.
Automated code review is less expensive
and can cover much more code in less time than manual review.
Indeed,
when a reviewer is tasked with reading and reviewing code manually,
line by line,
they are usually assigned only a particular piece or segment of code.
In the case of large products,
it would take a lot of time and effort to review all the code manually.
So,
this form of review generally has less scope
than that performed by intelligent machines,
but,
as we'll see,
it's an indispensable procedure given the limitations of the tools.

Automated tools have a database of predefined standards
and requirements for compliance review and error detection.
Organizations that purchase the tools can configure them
to follow specific rules and ignore others
and to work according to one or more specific programming languages.
The point is that
whatever is outside the predefined capabilities of the tool
escapes its detection radar.
Additionally,
not everything a tool reports truly represents an issue or flaw in the code.
We refer to these last two hurdles as false negatives (omissions)
and false positives (lies),
respectively.
Preventing these from being present
when making code review reports
is then in the hands of the experts and their manual work.

One of the biggest shortcomings of code review tools is their inability
to detect so-called business logic flaws.
Automated tools do not understand the human intentions
and business logic behind a particular system.
Business logic refers to the part of the software
that codifies business rules
that determine processes such as data creation,
modification and storage.
Business logic describes multiple series of activities or steps
in which relationships are established
between the end user interface and the database.
More often than not,
business logic flaws are peculiar to the application in question
and its functionality.
They are miscellaneous
and do not follow defined or similar risk patterns for all cases.
Moreover,
they are not located in a specific line of code
but involve several areas of the overall architecture.

The business rules dictate the software's responses or reactions
(e.g., prevention actions)
to the different possible scenarios.
Vulnerabilities in business logic often mean the inability of the software
to detect and correctly handle some scenarios,
certain strange or unexpected user behaviors
that the developers didn't take into account or anticipate.
That's where attackers capitalize on their cunning.
For example,
let's say
the logic in a money transfer application is not restricting user input
according to what might have been determined
in the business rules.
Instead,
it allows the entry of negative values,
which may lead to an unforeseen procedure such as,
let's imagine something,
extracting money from,
rather than depositing it to,
the supposed recipient of the transfer.
These types of vulnerabilities are often rated with very high severity
because of the potential impacts of their exploitation.
It is a task of the manual code review
to detect and report these enormously dangerous security issues.

Nevertheless,
on balance,
rather than considering substituting or replacing one method with the other,
we should speak of complementation.
Ideally,
we should use both methods,
not just one.
The automated code review,
with its scope and speed,
allows the time and effort invested in manual code review to be reduced.
It enables the expert to concentrate on pieces of code
that may have more complex and severe vulnerabilities
than those the machine can identify.
Unfortunately,
there are many who,
in their ignorance,
continue to believe that one or more automated tools
running in their organizations
is good enough.
They have not heeded comments like those
made in communities such as [OWASP](https://owasp.org/www-pdf-archive/OWASP_Code_Review_Guide_v2.pdf):
"manual code review should be a component of a company's secure lifecycle,
as in many cases it is as good,
or better,
than other methods of detecting security issues."

<cta-banner
  buttontxt="Read more"
  link="/solutions/secure-code-review/"
  title="Get started with Fluid Attacks' Secure Code Review solution right now"
/>

## Zeroed in on manual code review

The manual code review can be carried out by colleagues of the developers,
senior engineers or other professionals,
including external providers
such as Fluid Attacks with its [Secure Code Review](../../solutions/secure-code-review/).
The people in charge of a thorough code review
should have extensive knowledge of software development,
programming languages, [secure coding practices](../secure-coding-practices/),
security [standards](https://docs.fluidattacks.com/criteria/compliance/),
[requirements](https://docs.fluidattacks.com/criteria/requirements/)
and [vulnerabilities](https://docs.fluidattacks.com/criteria/vulnerabilities/),
among other things.
They should be able to [think and act like threat actors](../thinking-like-hacker/)
and have the virtue of patience
and vast review experience.
However,
some reviewers may be just beginning to gain experience
and should not be excluded
but may simply be assisted by other,
more seasoned individuals.
This decision,
in any case,
may vary according to the needs
and characteristics of the code
of the organization requesting the service.
Keep in mind,
as it's commented in the [OWASP Code Review Guide](https://owasp.org/www-pdf-archive/OWASP_Code_Review_Guide_v2.pdf),
for instance,
that "a new single sign-on authentication module
in a multi-billion dollar company
will not be secure code reviewed
by a person who once read an article on secure coding."

It's always recommended that
a single person doesn't do a manual code review.
What initially escaped the developer's eyes,
in some cases,
may also elude the reviewer's eyes.
Although with the inclusion of a second individual,
the same thing can also happen,
the probabilities would certainly be reduced.
Additionally,
work performed by several individuals promotes the creation
of a collaborative environment
between the members of the development and review teams.
Cooperation can occur
when the reviewer is not seen as a patrolman
but as an advisor
that positively affects the efficiency of the developers
with relevant feedback.
Reviewers should ask developers to send small code changes to them
for a better workflow.
And they can do reviews in environments
isolated from those in which the developers may be working
so they don't act as obstacles.

To conduct comprehensive and effective reviews,
experts must be in context,
knowing what they are assessing.
They must learn about and broadly understand the software's functions,
purposes and features to be evaluated,
including the programming languages
and libraries and other components used
and their interactions.
From there,
reviewers should ask questions
such as what might happen if some operation of the code fails.
They must know what types of users are allowed
and which are their privileges.
They must understand what kinds of data are being processed
and in what way
and ask what would happen if they were compromised.
In addition,
they must model potential threats,
in part recognizing threat agents and their possible purposes,
and,
depending on the type of software,
anticipate what security vulnerabilities they may find.

The amount of information to be gathered in a code review
will depend on the organization's size,
the reviewers' skills
and the potential risks of the code.
A good way to start this collection
may be to establish contact and conversation
with the application developers
to receive at least some basic information.
Automated tools also come into play
to provide general data
before the manual review is implemented on specific areas of the code
(prioritized, for example, by risk)
to assess style,
interpretation and security.
Tools such as linters can even be used in advance by developers
to get support in identifying simple formatting errors
such as typos.

In the code review,
keeping as support and guide the standards
set or requested by the organization,
including,
of course,
the business rules,
the reviewers will first learn about the architecture
and style of the code
and hence its errors.
Concerning the standards,
the reviewers can handle checklists of security requirements
adapted to the software design
that cannot be overlooked,
such as the following:
input validation, authentication and password management,
access control and session management,
cryptography and data protection,
error handling and logging,
system configuration and control,
among others.
The reviewers will mark out the attack surface
and possible attack vectors,
the security controls implemented so far
(how well are assets and operations being protected?),
the vulnerabilities present,
the estimated risks and possible impacts,
etc.
The categorization and qualification of vulnerabilities
are pretty useful
as they allow their prioritization
for the subsequent remediation
by the team of developers.

For each error or security issue detected in the code,
the reviewers must recommend a modification
to comply with the previously defined requirements.
If necessary,
they establish contact again with the development team
to initiate discussions
(e.g., about the feasibility of the suggested changes)
or to resolve doubts and difficulties.
Subsequently,
if required,
the reviewers propose alternative recommendations or solutions
and define exceptions to reach an agreement.
After incorporations or modifications by developers,
a new review may take place
to verify that they took suggestions on board
and that their product is now of better quality and security.

At Fluid Attacks,
we offer you our Secure Code Review
(for more details,
[read this post](../secure-code-review/)),
with automated and manual code review,
within an integral service called [Continuous Hacking](../../services/continuous-hacking/).
This service is not limited to [static application security testing](../../product/sast/)
and [software composition analysis](../../product/sca/).
Beyond the intervention of our automated tools
(we invite you to use them for [21 days for free](../../free-trial/)),
which also perform [dynamic application security testing](../../product/dast/),
we employ methods such as [manual penetration testing](../../solutions/penetration-testing/)
and [reverse engineering](../../product/re/)
with our highly certified ethical hackers.
For more information
on how we can help you prevent your organization
from falling victim to cyberattacks,
do not hesitate
to [contact us](../../contact-us/).
