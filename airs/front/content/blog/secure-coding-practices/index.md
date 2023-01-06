---
slug: secure-coding-practices/
title: Go Over and Practice Secure Coding
date: 2022-11-22
subtitle: And round it off with our Secure Code Review
category: philosophy
tags: cybersecurity, security-testing, software, company, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1669143333/blog/secure-coding-practices/cover_secure_coding_practices.webp
alt: Photo by Ga on Unsplash
description: Check out some best practices for secure coding your developers can start applying and how our Secure Code Review can complement them.
keywords: Secure Coding, Secure Code, Secure Coding Practices, Secure Coding Guidelines, Secure Code Review, Software, Security Vulnerabilities, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/XncszFVfqhE
---

It never ceases to be glaringly evident
how insecure the software used by individuals and organizations
in almost every industry on the planet
tends to be.
Just look at the news in The Record over the last month,
and you'll find cyberattacks targeting the [aviation](https://therecord.media/cyber-incident-at-boeing-subsidiary-causes-flight-planning-disruptions/),
[space](https://therecord.media/cyberattack-on-observatory-in-chile-raises-concerns-about-security-of-space-tech/)
and [education](https://therecord.media/michigan-school-districts-reopen-after-two-day-closure-due-to-ransomware-attack/)
industries
([as we saw recently](../what-trends-to-expect-for-2023/),
the latter is among the most attractive to threat actors today).
While it is true that many attacks are often successful
thanks to [social engineering](../social-engineering/)
(e.g., [phishing campaigns](../phishing/)),
many others achieve their goal
through [another major attack vector](https://www.ibm.com/reports/threat-intelligence/):
the exploitation of security vulnerabilities in software.

Here we are not discussing something
that affects only the small and the feeble.
Large companies that provide software as a product or service
(recent examples: [Google](https://therecord.media/google-chrome-d-link-bugs-among-twelve-added-to-cisas-list-of-known-exploited-vulnerabilities/),
[Siemens](https://therecord.media/critical-vulnerability-found-in-siemens-industrial-tool-allowing-theft-of-cryptographic-keys/),
and [Microsoft](https://therecord.media/microsoft-confirms-dogwalk-zero-day-vulnerability-has-been-exploited/)),
as well as well-known organizations that make use of software
(recent examples: [a federal agency](https://therecord.media/suspected-iranian-apt-accessed-federal-server-via-log4j-vulnerability/),
[Aurubis](https://therecord.media/worlds-second-largest-copper-producer-recovering-from-cyberattack/),
and [Mitel](https://therecord.media/initial-access-broker-or-ransomware-gang-has-exclusive-access-to-mitel-zero-day-exploit-report/)),
continue to be seriously impacted by cyberattacks.
Many vulnerabilities exploited by malicious hackers
to steal information or disrupt operations
are found in the applications' source code
(i.e., those instructions that define their structure and functionality
and are interpreted by devices).
This is why one of the best ways
to prevent cyberattacks and their impacts
is to develop software products correctly,
writing secure source code
from the beginning of the software development lifecycle (SDLC).

## What is secure coding?

Secure coding or secure programming is the software development practice
in which the occurrence of programming errors
that give rise to security vulnerabilities
is avoided.
This activity implies a high knowledge of the programming language in use
and the judicious following of conventions and principles
or secure coding standards.
This is why
the development teams of any company interested in its cybersecurity
must be trained in this regard.

It is problematic that
many developers see the inclusion of security principles
in software development
as a hindrance.
One of the causes of this is the continuous demand
for rapid delivery of products and new features within them.
[In their rush](../do-not-read/)
to respond quickly to customer or user requests,
sometimes led by managers apathetic about a cybersecurity culture,
[developers brush aside](../pii-leakage-whitehat/)
risk exposure.
In other cases,
they may be asked or compelled to pay attention to security,
but simple factors such as lack of focus or unfamiliarity
can also impede secure coding.
Software developers' lack of cybersecurity knowledge is [commonplace today](https://www.securityjourney.com/post/how-do-you-practice-secure-coding),
so much so that they can ignore,
for instance,
the existence of public standards such as [OWASP](../../compliance/owasp/).
Actually,
a first step to prevent security vulnerabilities
may be to keep standardized vulnerability databases
such as [CWE](../../compliance/cwe/),
[CERT](https://docs.fluidattacks.com/criteria/compliance/certc),
[CVE](../../compliance/cve/),
[OWASP](https://docs.fluidattacks.com/criteria/compliance/owasp10)
and [PA-DSS](https://docs.fluidattacks.com/criteria/compliance/padss),
among others,
at hand and under review.
(Check also our set of [vulnerability types](https://docs.fluidattacks.com/criteria/vulnerabilities/).)

Organizations that develop and offer software as a product or service,
and have not yet done so,
must begin to create or reinforce a security-based culture
within their units.
This is where the now celebrated [DevSecOps approach](../devsecops-concept/)
comes in,
where security should be the responsibility of all team members
and not just something for a security team.
Although it can be a complex and time-consuming change,
it is a worthwhile effort in terms of costs and chances of success,
and in which the so-called Security Champions
(of which [we've already spoken about](../secdevops-security-champions/))
can step in.
As we'll see below,
the work of developers can be significantly assisted by security testing.
However,
it's still essential they understand
what they're doing in terms of risks and threats,
know where they are making mistakes,
and begin to keep **practices** that enable them to avoid these failures
and,
consequently,
the appearance of vulnerabilities in their products.

## Some secure coding practices

It's easy to find secure coding best practices
or guidelines on the Internet
(e.g., [OWASP DevGuide](https://github.com/OWASP/DevGuide),
[Microsoft Writing Secure Code](https://learn.microsoft.com/en-us/previous-versions/msdn10/aa570401(v=msdn.10)),
[Red Hat Secure Coding Tutorials](https://developers.redhat.com/topics/secure-coding)).
For this post,
we partly took as a basis [Secure Coding Practices - Quick Reference Guide](https://owasp.org/www-pdf-archive/OWASP_SCP_Quick_Reference_Guide_v2.pdf)
from OWASP
(we recommend you check it for more details)
and added other considerations
and some valuable tips worth mentioning.
(Check also our set of [security requirements](https://docs.fluidattacks.com/criteria/requirements/).)

### Security from the first line of code

It's imperative to start
with the idea of not leaving security for the end of the SDLC.
Thinking about and acting in favor of a secure software product
from the first line of code
makes it possible to avoid subsequent high costs.
Not only costs in the remediation of vulnerabilities
(these are much lower in the development phases
than in the final ones or in production)
but also those arising from their exploitation,
in other words,
security breaches.
Developers shouldn't have as their sole objective
the rapid release to production of a product
with optimal functionality.
Among their main purposes,
they should include delivering high-quality software
that guarantees security.

### Thinking like threat actors

Developers should try to look at their creations
as if they were malicious hackers themselves.
(We once wrote a post entitled [Think Like a Hacker!](../thinking-like-hacker/)
which may serve as a reference in this regard).
They should not only focus on the purposes and use cases of the product
but also on how criminals could exploit it
in case of having vulnerabilities.
Developers should be clear
about which assets and operations would be attractive to threat actors.
They should be aware of potential threats and risk levels
and keep in mind and practice preventive measures.

<cta-banner
  buttontxt="Read more"
  link="/solutions/secure-code-review/"
  title="Get started with Fluid Attacks' Secure Code Review solution right now"
/>

### Input validation

The mere use of the developed application or software,
specifically the input of data,
usually represents a risk.
For example,
attacks known as [SQL injection](../sql-injection/)
and [cross-site scripting (XSS)](../xss-protection/)
can occur due to vulnerabilities
arising from trusting external data sources and user input,
whereby the software does not distinguish between commands and data.
In other words,
certain characters can enter the application
functioning as malicious code
and cause it to behave abnormally
or in a way that deviates from its intended operation.
Hence the need to continuously validate
what enters the software product.

Developers must ensure that
data sources are classified as trusted and untrusted.
Their product must validate the input
(mainly)
from untrusted sources appropriately.
It must verify the properties of the incoming data
and accept only those inputs that comply with specific characteristics
(e.g., type, range, length, allowed characters).
If the inputs do not comply with them,
the application must reject them.
To this process,
developers should add [output encoding](https://sites.google.com/site/iasoncs/home/defensive-programing/output-encoding),
in which all untrusted input is transformed to a safe form,
remains as data,
and is not executed as code.

### Authentication and password management

The software must verify
through a standardized process
the identity of the user or entity that interacts with it,
especially when trying to access resources
that are not intended to be public
or external systems with confidential material.
Authentication failures should generate responses
that do not specify which of the requested data were erroneous or invalid.
Critical operations such as money transfers,
for example,
should request re-authentication or multi-factor authentication.

If the application stores credentials,
developers should ensure
they are always cryptographically one-way solid [hashes of passwords](../pass-cracking/).
To strengthen the [complexity of passwords](../credential-stuffing/)
([preferably passphrases](../requiem-password/)),
the application should require users to include numbers
and special characters
in addition to lowercase and uppercase letters in them.
After a few unsuccessful login attempts by a user,
the software should deactivate that account for a specific period.
Additionally,
password modification should be properly controlled,
and the application should notify the user each time it occurs.

### Access control and session management

In addition to user identity verification,
the product must have a process
that allows or denies access to resources.
Developers should restrict access to certain resources
(including protected URLs, functions, services, files, and critical data)
to only a few authorized users.
They should always apply the principle of least privilege.
By default,
access must be denied,
and the system must maintain and verify conditions or characteristics
(beyond role verification)
to allow it.
Ideally,
the software should restrict users to access only the resources
necessary to accomplish their tasks or jobs.
In a given period,
the number of transactions by a user or entity should be limited
and unused accounts should be deleted.
Moreover,
developers should set session inactivity timeouts
to be as short as possible,
not allow simultaneous logins with the same account
and generate new session IDs to replace the old ones periodically.

### Cryptography and data protection

Data protection or confidentiality
depends heavily on the use of well-known,
well-vetted and up-to-date encryption algorithms
for sensitive data in transit and at rest.
In line with what was mentioned above for passwords,
they and no other sensitive information should be stored in clear text
or any other form that doesn't involve [cryptography](../post-quantum-cryptography-algorithms/).
In code that may be accessible to users
(server-side source code should not be allowed to be downloaded by users),
developers should remove comments
that reveal confidential information.
The same should be done with unnecessary documentation about the application.
The software product must also support removing sensitive data
when it's no longer useful.
This same kind of information shouldn't be present in cookies,
and handling such data shouldn't lead to the generation of cached copies.

### Error handling and logging

Related to what we mentioned for authentication failures,
invalid activities in the application or product
may generate error messages.
The idea is that these messages should not reveal information
that could be useful to potential attackers
(e.g., session identifiers, system details or account information).
This same information should not be stored in logs.
Logging of events that occur in the code allows the identification of errors.
Actions that cause application failures
(e.g., input validation, authentication, access control,
administrative functions, cryptographic modules)
should be logged and blocked.
Developers should restrict access to all logs
only to a group of authorized users.

### System configuration and control

Developers must ensure that servers,
frameworks and other system components are at their latest verified versions
with all relevant security patches applied.
In addition,
all unnecessary application files and components
(e.g., from third-party code)
should be removed.
This is somewhat connected to the idea of keeping the code and systems
as clean and simple as possible.
By reducing the complexity of the product,
including only what is really necessary,
developers reduce the likelihood of security vulnerabilities emerging.
Additionally,
it is recommended that
they maintain the use of systems for source code control
and careful tracking of changes.

## Secure code review

The above are just a few recommended practices for secure coding.
For them,
there is an almost indispensable complement
that allows developers to guarantee
the high quality of their software products.
This is security testing,
especially in secure code review mode.
[In a recent blog post](../secure-code-review/),
we described this type of test
and the benefits it can bring to an organization that develops software.
Essentially,
it is a contribution by an external provider,
such as Fluid Attacks,
in which automated tools and humans
(some providers mistakenly restrict themselves to the use of tools)
have the mission to detect security vulnerabilities
in the source code.

While groups of developers can educate themselves
or receive training on practices such as those outlined above,
it is not surprising that bugs and vulnerabilities continue to appear
in their work over time.
Through [Fluid Attacks' Secure Code Review](../../solutions/secure-code-review/),
which involves our tools and our team of ethical hackers
with techniques such as [SAST](../../categories/sast/)
and [SCA](../categories/sca/),
and in which we support around 40 programming languages
and use more than [60 international security standards](https://docs.fluidattacks.com/criteria/compliance/)
as a basis for assessment,
we report to your development teams such security issues
that arise in their constructions.
[As we've said before](../devsecops-best-practices/),
these reports serve as feedback to them,
and the practice of remediating identified vulnerabilities
nurtures their knowledge of secure coding.
Although the occurrence of errors will indeed not cease,
they will be able to notice and fix them more easily.

As software tends to evolve at an incredible pace to meet users' needs,
we offer Secure Code Review as part of our [Continuous Hacking service](../../services/continuous-hacking/).
In this constant process,
we are attentive to all the changes in your repositories,
and we add techniques beyond the secure code review,
such as dynamic application security testing ([DAST](../../categories/dast/)).
[Contact us](../../contact-us/)
if you want to find out
what your development teams are overlooking
and what is putting your organization at risk.
[Register here](../../free-trial/)
if you want to start
with a 21-day free trial of continuous security testing
by our automated tools.
