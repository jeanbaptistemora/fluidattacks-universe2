---
slug: owasp-top-10-2021/
date: 2021-10-04
subtitle: New OWASP Top 10 emphasizes secure design
category: philosophy
tags: risk, web, application, trends, security, standard
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1633374808/blog/owasp-top-10-2021/cover_owasp.webp
alt: Photo by Mathew Schwartz on Unsplash
description: The OWASP Top 10 ranks the most critical security risks
    to web applications. The 2021 installment comes with new categories,
    name changes and a new order.
keywords: Owasp, Top, Ten, Compliance, Web, App, Security,
    Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/3z56aMRpjJ0
---

The Open Web Application Security Project (OWASP) Top 10 is a ranking of
the most critical security risks to web applications. It was first
created as an awareness document, with the objective of motivating
software developers to produce more secure code. Today, its importance
is so huge that it’s considered a requirements document when it comes to
web application security.

This year’s new installment is the result of applying a new methodology
and name changes, merging categories and finding new ones. Most
importantly, it has revealed a new order that highlights different
issues, like secure design and threat modeling.

## New times call for new ways

This year’s Top 10 is based on a massive amount of data provided by
different sources since 2017. The sources were as varied as
organizations doing internal testing, organizations that test vendors by
trade and bug bounty vendors. But, in a refreshing way, this installment
now acknowledges the importance of the input provided by application
security and development experts. The reason is that they have proven to
be aware of trends that are not in the data produced by automated tools.
These trends may be found only with new creative ways of testing, which
take time to integrate into tools and processes. So, leaving the
expert’s account out of the list may result in an outdated ranking,
which is not the point of the Top 10 at all. With this reason in mind,
two of the categories in the list came from the results of a community
survey asking experts what they see as essential weaknesses that may not
yet be found in the data.

As in 2017, the new installment used data that was collected and
analyzed along the lines of incidence rate. This means that instead of
counting every time a vulnerability shows up in a single application, it
would only be counted as one. This seems to resolve the problem that
some vulnerabilities that appear a ton of times in automated tools
obscure the importance of some other serious vulnerabilities.
Additionally, in 2021, a change in data collection was made, so that
organizations could provide more data on Common Weakness Enumerations
(CWEs), that is, categories of unknown custom weaknesses. Instead of
being provided a restricted list of CWE categories to report,
organizations were able to report any new weaknesses without
restrictions.

Another noticeable difference is the change in some categories' names.
These changes mirror an increased interest in the root cause as opposed
to the symptoms. The rationale behind this is that, by conceding more
visibility to the root causes, more attention can be directed to
identification and remediation.

## A new order

<div class="imgblock">

![OWASP Top 10 2017-2021](https://res.cloudinary.com/fluid-attacks/image/upload/v1633374808/blog/owasp-top-10-2021/figure-owasp.webp)

<div class="title">

Figure 1. OWASP Top 10 [2017 and 2021
comparison](https://owasp.org/Top10/A00_2021_Introduction/)
(taken from [owasp.org](https://owasp.org/Top10/assets/mapping.png)).

</div>

</div>

The new Top 10 shows how, as technology and development styles evolve,
risks have increased or decreased. In a worryingly impressive climb to
the first place from its previous spot at number five, [Broken Access
Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) is the
riskiest security flaw. This means that developers are failing to
implement proper access control and testing its functionality. The
situation is not pretty, with the worsening of the next category,
[Cryptographic
Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/),
previously known as Sensitive Data Exposure, its consequence. It shows
that more effort should be put into identifying sensitive information
and protecting it with up-to-date encryption techniques.

Although [Injection](https://owasp.org/Top10/A03_2021-Injection/) had
its thunder stolen by the previous two, it keeps being extremely
problematic. It has [many
faces](https://capec.mitre.org/data/definitions/152.html), which have
been recognized in previous installments of the Top 10. It had been
number one for a whole decade and now even includes [Cross-Site
Scripting](https://owasp.org/www-project-top-ten/2017/A7_2017-Cross-Site_Scripting_\(XSS\).html).
The risk of Injection persists as developers still use interpreters,
where the mixing of code and data is very common and results in
vulnerabilities.

The highest-ranking of this year’s new additions is [Insecure
Design](https://owasp.org/Top10/A04_2021-Insecure_Design/), in fourth
place. It refers to the lack of security controls to defend against
attacks and failure to establish a secure development lifecycle. This
flaw should not be taken lightly. There is a huge overlap with higher
rated risks, like Broken Access Control and Cryptographic Failures, and
some that are not so high up, like Identification and Authentication
Failures. These risks are part of an insecure design. This means that
now, more than ever, implementing secure design is not an option; it’s a
must. What developers should achieve is, following OWASP’s
recommendation, "a culture and methodology that constantly evaluates
threats and ensures that code is robustly designed and tested to prevent
known attack methods." This calls for the importance of [threat
modeling](https://owasp.org/www-community/Threat_Modeling), defined by
OWASP as "a view of the application and its environment through the lens
of security."

Moving down the list, [Security
Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
went up one place and appears merged with the XML External Entities
([XXE](https://owasp.org/www-project-top-ten/2017/A4_2017-XML_External_Entities_\(XXE\).html))
improper restriction issue, which is also considered a problem of
configuration. This and the following category, [Vulnerable and Outdated
Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/),
which moved up several places and had its name revamped, remind us of
the growing importance of properly configuring and upgrading the
application’s components, while also defending against attacks where
there are known vulnerabilities.

Number seven, [Identification and Authentication
Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/),
previously known only as Broken Authentication, poses at least a
redeeming quality of development over the last years. Namely, that this
category’s dramatic drop from second place means that the problem is
being tackled, perhaps through growing implementation of multi-factor
authentication, password complexity, limited failed login attempts,
among others.

Another new addition, at number eight, seems to be motivated by the
appalling impact of the [SolarWinds security
fiasco](../solarwinds-attack/). The risk of [Software and Data Integrity
Failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)
urges developers to verify integrity in the entire software build chain.
This not only means that the components used to build the applications
should come from trusted sources and be digitally signed. It also means
that attention should be directed to how suppliers are managing their
supply chain to provide integrity to their software. The merging of
[Insecure
Deserialization](https://owasp.org/www-project-top-ten/2017/A8_2017-Insecure_Deserialization.html)
with this category stresses the importance of also ensuring data
integrity by validating almost every bit of data.

At number nine, [Security Logging and Monitoring
Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
had a subtle name change and moved up one place. This category was also
supported by the results from the community survey. It reminds us of the
importance of implementing run-time protection to detect attacks and
create visibility into who is attacking, which, again, brings us back to
secure design.

The last new addition, at number 10, comes mainly from the community
survey. Experts are trying to raise awareness that Server-Side Request
Forgery
([SSRF](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/))
is a thing. It happens when there is no proper validation of the
user-supplied URL, which allows the attacker to make the application
send a crafted request to an unsuspecting destination.

That is the end of the list. Now, are you ready to tackle the challenge
ahead? At `Fluid Attacks`, we help you with OWASP compliance by
implementing security at the development stage of your web applications.
[Contact us](../../contact-us/)\!
