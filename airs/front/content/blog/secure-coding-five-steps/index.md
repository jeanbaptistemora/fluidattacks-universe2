---
slug: secure-coding-five-steps/
title: Secure Coding in Five Steps?
date: 2022-12-05
subtitle: A simple approach to try out in cybersecurity training
category: opinions
tags: cybersecurity, security-testing, software, company, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1670296878/blog/secure-coding-five-steps/cover_secure_coding_five_steps.webp
alt: Photo by Ralston Smith on Unsplash
description: We present a short review of a study in which the authors suggest an approach to introduce and encourage software developers to use secure coding practices.
keywords: Secure Coding, Secure Code, Secure Coding Practices, Software Development, Secure Code Review, Five Steps, Security Vulnerabilities, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/zc9pWsPZd4Y
---

There's still a shortage of education in cybersecurity.
There's still a lack of workforce generation in this area.
As reported in the [(ISC)² 2022 Cybersecurity Workforce Study](https://www.isc2.org//-/media/ISC2/Research/2022-WorkForce-Study/ISC2-Cybersecurity-Workforce-Study.ashx),
there is currently a "worldwide gap of 3.4 million cybersecurity workers".
On the software development side,
many professionals are unfamiliar with the subject
and deliver products that sometimes don't even undergo
(at least adequate)
review.
Secure coding and secure code review,
or better yet,
an entire secure development cycle,
should be taught to developers
from the beginning of their careers.
While their work is usually supported by other teams
(such as one specifically for security),
security-savvy developers can contribute early on
to making their products high quality and consequently secure.
We must seek to leverage existing resources
and create methods that contribute to their training.
In this post,
we focus precisely on a simple approach
recently suggested in a research article.

## "Secure Coding in Five Steps"

While roaming the Internet
looking for a topic to round out a short series of five posts
regarding the concept of "[secure code review](../../solutions/secure-code-review/),"
an article called "Secure Coding in Five Steps" caught my attention.
(Incidentally,
the posts in that series are
"[Do You Apply Secure Code Review?](../secure-code-review/),"
"[Go Over and Practice Secure Coding](../secure-coding-practices/),"
"[Indispensable Manual Code Review](../manual-code-review/),"
"[Code Quality Must Include Security](../code-quality-and-security/)"
and this one you're currently reading).
Published in mid-2021 by Zeng and Zhu
in the *Journal of Cybersecurity Education, Research and Practice*,
this is a free and open-access article
that you can find and review in full
at [digitalcommons.kennesaw.edu](https://digitalcommons.kennesaw.edu/jcerp/vol2021/iss1/5/).

More specifically,
I came to this article
because I was thinking about and looking for information on standards,
courses and training for secure coding.
As the authors begin by saying in the abstract,
"There are numerous resources of industry best practices available,
but it is still challenging to effectively teach secure coding practices."
Material is what we have.
And in overwhelming abundance.
With my now almost three years in the cybersecurity field,
I have witnessed it.
Following the authors of the paper in question,
the problem with these resources,
such as testing guidelines,
vulnerability databases and secure coding standards,
is that they are not intended or developed directly for academia
and its students.

As is undoubtedly already known to many of us,
education on cybersecurity issues within universities is still feeble.
Over the years,
efforts have been made to include courses
in secure software development or secure coding
in several institutions' computer science curricula
and even to make public online material for learning.
All of this is aimed at dealing with the growing threats and risks
in a cyber universe that is increasingly crowded
with interconnected information systems
and cybercriminals looking to take advantage of them.

What the researchers in the article referenced here intend to do
is to bring about an improvement in this situation.
They start from the fact
that it's from the beginning of the development of software products
that trainees and professionals must think
and act in terms of security.
They present a **five-step approach to learning**
that is more suitable for students,
less complex,
and that motivates them to practice secure coding.
"The long-term goal is to educate students
on the right mindset,
necessary knowledge,
and skills to develop secure software,"
say the authors.
In their research,
they didn't merely share theory
but put it into practice with their own undergraduate and graduate students
in their computer and software security course.
Let's take a look at each step with its background
and what these researchers' methodology was like in action.

### Before the first step

Although we could speak of a "step zero,"
the researchers didn't name this first procedure.
Perhaps because it's not focused on secure coding per se.
What they did initially,
before the first step,
was to give the students a broad landscape in secure development,
using as a reference the [Microsoft Security Development Lifecycle (SDL)](https://www.microsoft.com/en-us/securityengineering/sdl/practices).
This is a set of 12 practices
that promote secure software development
(practices closely connected with what we do at Fluid Attacks):

1. [Provide training](../training-basic/)
2. Define [security requirements](https://docs.fluidattacks.com/criteria/requirements/)
3. Define metrics and [compliance reporting](https://docs.fluidattacks.com/criteria/compliance/)
4. Perform threat modeling
5. Establish design requirements
6. Define and use cryptography standards
7. Manage the security risk of [using third-party components](../sca-scans/)
8. Use approved tools
9. Perform static analysis security testing ([SAST](../../categories/sast/))
10. Perform dynamic analysis security testing ([DAST](../../categories/dast/))
11. Perform [penetration testing](../../solutions/penetration-testing/)
12. Establish a standard [incident response process](../incident-response-plan/)

To meet the need for hands-on training
(practicing the five steps in secure coding),
the researchers decided to use a simple web application called ShareAlbum.
Developed by other students
using PHP, HTML and MySQL,
this app allows sharing of photos and videos among its users,
as well as messages.
Files within ShareAlbum can be categorized as public or private
and reviewed, commented and tagged by users
depending on preset privileges.
The authors then presented this app in detail
to the students participating in the study.

### First step

This step is aimed at **gaining knowledge
about common security vulnerabilities**.
The [CWE Top 25](https://docs.fluidattacks.com/criteria/compliance/cwe25)
most dangerous software weaknesses
and the [OWASP Top 10](https://docs.fluidattacks.com/criteria/compliance/owasp10)
most critical web application security risks
come into play.
The authors introduced these lists
(in addition to the Common Vulnerabilities and Exposures, [CVE](../../compliance/cve/))
to their students.
They then selected three types of vulnerabilities
(i.e., [Cross-site scripting](https://docs.fluidattacks.com/criteria/vulnerabilities/008),
[SQL injection](https://docs.fluidattacks.com/criteria/vulnerabilities/146)
and [Unrestricted upload of file with dangerous type](https://docs.fluidattacks.com/criteria/vulnerabilities/027))
and explained in depth their characteristics,
exploitation mechanisms,
potential impacts and detection and remediation methods.
Afterward,
to vividly illustrate all this,
the researchers used ShareAlbum as an example of software
with these vulnerabilities.
As part of their active participation,
the students had to review the other vulnerabilities on the lists,
choose two and explain them briefly to their classmates.
In addition,
the students were given small pieces of code from ShareAlbum
to detect and remediate vulnerabilities
of the three types initially discussed.

### Second step

This step is aimed at **acquiring skills
in security testing or vulnerability identification**.
The authors recognize manual code review as indispensable
and the benefits of mixing this method with automated tools
(for their scalability and speed).
For this reason,
they assigned small groups of students
to detect errors in the app's code
by manually following a checklist
(adapted from the OWASP Code Review Guide)
and using a free SAST-type tool,
to which they were duly introduced.
The list of security issues that the students were able to assemble
included errors such as improper input validation,
improper authorization and information exposure.
In their exercise with the automated tool,
the students were made aware of its shortcomings,
such as the existence of false positives and false negatives,
and educated in their identification and solution.
After that,
they were able to practice recognizing and reporting the false positives
provided by the tool
in its list of identified errors.

<cta-banner
  buttontxt="Read more"
  link="/solutions/secure-code-review/"
  title="Get started with Fluid Attacks' Secure Code Review solution right now"
/>

### Third step

This step is oriented to the **prioritization of vulnerabilities**.
The researchers shared with their students that
remediation of all vulnerabilities can be costly,
so they should be prioritized according to different attributes.
It will always be more beneficial
in terms of risk and resource management
to strive to close some vulnerabilities before others.
Therefore,
the students were introduced to the Common Vulnerability Scoring System
(CVSS; at Fluid Attacks,
due to a couple of defects in this system,
we modified it slightly to become "[CVSSF](../cvssf-risk-exposure-metric/)").
The authors taught the students the use of metrics
(e.g., exploitability and impact)
for calculating CVSS scores
and ranking and labeling vulnerabilities.
Then,
the students used the CVSS calculator
for the vulnerabilities they had previously detected in the app.
From there,
they prioritized vulnerabilities according to the scores obtained
and provided the top three errors
to be remediated in the next step.

### Fourth step

This step is aimed at **vulnerability remediation and risk mitigation**.
The remediation suggestions
provided by the CWE and OWASP websites and the SAST tool
were considered.
The authors took the three vulnerabilities they used as examples
and presented the students with their step-by-step remediation in ShareAlbum.
Next,
the students took their top three security issues or errors
from the previous step,
discussed remediation strategies
and then applied them as code changes.
Finally,
they performed another code review
to see if those modifications had been effective
and if they had resulted in new vulnerabilities,
which would need to be remediated.

### Fifth step

This last step is oriented to the **reporting or documentation of results**.
Recognizing the frequent use of standard report templates in industries,
the researchers put together a template
based on "the OWASP secure coding report items
and the MITRE secure code review sample."
The students had to submit a report following the template,
which had nine items,
including review dates,
code modules reviewed,
checklist and tool used,
vulnerabilities identified
and the top three of these
(each with details such as name,
description, location, severity and remediation strategy),
among others.
(For example,
you find all that kind of data
when you receive reports in the Fluid Attacks'
[Attack Resistance Management platform](../from-asm-to-arm/)).

## Conclusions and opinions

The actual contributions of this five-step approach are not very clear.
The authors only spoke of having conducted surveys of students
before and after the training.
(You can see the paper
to know the characteristics of the participants
and the results in numbers).
Although it doesn't give the impression of having been highly rigorous work,
especially in collecting and analyzing data,
I'm not the one to evaluate or criticize it.
What this study leaves us with is that,
apparently,
the students after the training,
according to their feedback,
were more motivated to review and apply secure coding guidelines,
standards and practices
(including error reporting and remediation)
in their future software development work.
In addition,
most of them felt comfortable with the training approach
and the case studies.

As I was reading this article,
it seemed to me that
it was very much in line with what we have offered
in previous secure code review posts
and, in part, our way of working at Fluid Attacks
in software assessment.
I don't know if this five-step approach is the best way
to introduce software developers to secure coding practices and skills.
Still,
it is definitely a worthwhile approach
(the researchers say they are improving it further,
for example,
by broadening the spectrum of programming languages used).
I thought it was a good idea
to start by giving students a "big picture of secure coding,"
exposing them to the many resources available
(other examples: [OWASP SAMM](https://try.fluidattacks.tech/report/owasp-samm/),
SAFEcode and CERT standards),
as well as giving them lots of examples
and, above all, "hands-on opportunities."
From universities and companies,
we should encourage learning in secure software development
with proposals like this
that serve as part of a preventive strategy
against today's growing cyber threats.
We invite you to review Zeng and Zhu's paper thoroughly
to get more details about their suggested approach.

Now,
if you are looking for support
for the development teams in your organization
by security experts,
do not hesitate to [contact us](../../contact-us/).
At Fluid Attacks,
we offer [Secure Code Review](../../solutions/secure-code-review/)
within our [Continuous Hacking service](../../services/continuous-hacking/)
that mixes automated tools with expert intelligence
to detect vulnerabilities in your software.
If you want a first taste of our cybersecurity capabilities,
we invite you to enjoy [SAST](../../categories/sast/),
[DAST](../../categories/dast/)
and [SCA](../../categories/sca/) techniques
with our automated tools
in our [21-day free trial](../../free-trial/).
