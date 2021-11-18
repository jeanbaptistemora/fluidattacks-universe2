---
slug: human-security-sensor/
title: Your Ally Is Closer Than You Think
date: 2021-10-26
subtitle: Employees as the strongest link in the security chain
category: philosophy
tags: cybersecurity, risk, mistake, social-engineering, training, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1635285831/blog/human-security-sensor/cover_haass.webp
alt: Photo by Andre Mouton on Unsplash
description: The human-as-a-security-sensor paradigm asserts that catastrophe
  can be prevented if employees are trained to report threat events promptly.
  Learn more here.
keywords: Human, Security, Sensor, Employees, Risk Factors, Weakest Link,
  Reporting, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/GBEHjsPQbEQ
---

You may have already heard that humans are the weakest link in corporate
information security. It is difficult to convince you otherwise when
there is strong evidence for this claim. To name a few examples, only
51% of respondents of an [international
survey](https://www.proofpoint.com/sites/default/files/threat-reports/pfpt-us-tr-state-of-the-phish-2021.pdf)
conducted last year knew that they should treat any unsolicited email
with caution, 55% knew that an email can appear to come from someone
other than the true sender and 58% knew that attachments can be infected
with dangerous software. Also, 34% of US respondents reported they
believe emails with familiar logos are safe. Furthermore, users can be
easily manipulable through a set of [weapons of
influence](../social-engineering/) used by social engineers, who collect
sensitive data and plan to infect devices with malware. Likewise,
researchers have
[identified](https://www.faa.gov/about/initiatives/maintenance_hf/library/documents/media/human_factors_maintenance/human_error_in_aviation_maintenance.pdf)
a list of human errors, referred to as the "dirty dozen," which could
lead to security risks: group norms, complacency, distraction, fatigue,
pressure, stress, as well as lack of communication, knowledge, teamwork,
resources, assertiveness and awareness.

Although there may be complex causes of human error, such as the work
environment and individual differences, most of the attention has been
paid to security awareness. The latter is such a huge deal that employee
training is one of the security controls that show [companies
care](https://www.gartner.com/en/articles/4-metrics-that-prove-your-cybersecurity-program-works)
about cybersecurity. Also, training and education have been suggested as
preventive measures against
[phishing](https://www.proofpoint.com/sites/default/files/threat-reports/pfpt-us-tr-state-of-the-phish-2021.pdf)
and
[ransomware](https://www.proofpoint.com/sites/default/files/e-books/pfpt-us-eb-2021-ransomware-survival-guide.pdf).
A [Ponemon
research](https://www.proofpoint.com/sites/default/files/analyst-reports/pfpt-us-ar-ponemon-2021-cost-of-phishing-study.pdf),
conducted in the US with 591 IT and IT security practitioners from
organizations (44% of which have 1,000 or more employees), calculated
that the average cost of phishing is almost $15M annually. Respondents
estimated that this cost can be reduced by an average of more than half
if training is conducted.

On the verge of closing this Cybersecurity Awareness Month, we would
like to explain how employees may be the strongest link for early
detection of attacks that involve deception. Authors [Vielberth, Menges
and
Pernul](https://cybersecurity.springeropen.com/articles/10.1186/s42400-019-0040-0)
describe the human-as-a-security-sensor paradigm, which shows how
employees can detect anomalies and potential risks, and further show how
to integrate human reports in technical security systems. Here, we will
only focus on the former.

## What is human-as-a-security-sensor?

The human-as-a-security-sensor paradigm leverages the ability of human
users to act as sensors that can detect and report information security
threats. The utility of this paradigm is illustrated by Vielberth et al.
by means of a real-world example. Figure 1 shows a simplification of the
steps followed by several cybersecurity incidents that go by the name of
DarkVishnya. In these events, investigated by Kaspersky Lab between 2017
and 2018, attackers physically entered organizations, claiming to be a
person with a legitimate interest (e.g., being an applicant). Then, they
placed network devices unobtrusively and connected them to the local
network infrastructure. After leaving the physical premises, attackers
accessed their devices by utilizing standard mobile technologies. They
scanned for open resources like shared folders, servers or other systems
that execute critical actions. Finally, they used their gained access to
install malware.

<div class="imgblock">

![HaaSS steps](https://res.cloudinary.com/fluid-attacks/image/upload/v1635290618/blog/human-security-sensor/haass-figure-1.webp)

<div class="title">

Figure 1. How a human sensor could have detected earlier attack steps. Source: [media.springernature.com](https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs42400-019-0040-0/MediaObjects/42400_2019_40_Fig1_HTML.png?as=webp).

</div>

</div>

Vielberth et al. note that "the first three steps are nearly impossible
to detect with technical security systems \[…​\] as neither the attacker
entering the building, nor the placing of a hardware device leave any
digital traces." The first two, however, may be seen by employees. Here
is where they become the strongest link. Granted they are already
previously trained, employees can identify a new person in the building
and describe their appearance and suspicious actions, or they may be
able to detect a new device. Of course, there is a limit to what
employees may be able to report.

## What can employees as human sensors detect?

In Vielberth et al.'s model, human sensors can detect threat sources,
threat events, affected entities and estimate expected impact. These
risk factors, depicted in Figure 2, are based mainly on most of those
described in the [NIST
Guide](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-30r1.pdf)
for Conducting Risk Assessments. Following the authors' model, **threat
events** are the mandatory elements to report any anomaly. Threat events
can be intentional, like an attack, or unintentional, like technical,
environmental or legal incidents. Even though the initiation of a threat
event may be attributed to a threat source, the cause may also be a
previous event. It is also possible that at that moment nothing has been
affected, or at least the affected entities are not known yet and
neither is the impact.

<div class="imgblock">

![Taxonomy](https://res.cloudinary.com/fluid-attacks/image/upload/v1635290618/blog/human-security-sensor/haass-figure-2.webp)

<div class="title">

Figure 2. Taxonomy of risk factors inspired by the NIST Guide. Source: [media.springernature.com](https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs42400-019-0040-0/MediaObjects/42400_2019_40_Fig3_HTML.png?as=webp).

</div>

</div>

An employee may provide intelligence about physical access of outsiders,
suspicious emails or calls, which may involve [identity
spoofing](https://capec.mitre.org/data/definitions/151.html) (i.e.,
someone assuming the identity of some other entity) and [information
elicitation](https://capec.mitre.org/data/definitions/410.html),
[content
modification](https://capec.mitre.org/data/definitions/148.html) (e.g.,
changes to the source file of a webpage), or even physical damage of
organizational facilities from outsiders or insiders.

Employees can also make a relevant contribution to attribution by
identifying **threat sources**, like privileged insiders, competitors,
suppliers or nations that could be potential attackers. A threat may
also be legal in nature if information sharing policies in place do not
effectively safeguard sensitive information. Further, sources need not
involve humans, so employees may inform of events like failures of
equipment or software due to aging.

It is also possible for an employee to report or predict the **affected
entities**. Threat events can do potential harm to organizational
operations and relevant assets. Moreover, they could damage an
organization’s reputation or result in substantial financial costs.
Individuals may also be the affected ones, as is the case in identity
theft. However, the affected entities may also be other organizations or
even the whole nation.

Finally, the **expected impact** can be evaluated using the NIST Guide,
which provides qualitative ratings depending on the extent and duration
of the degradation in mission capability, the damage made to assets,
financial loss and harm to relations. So, for example, if the resulting
degradation in mission capability is such that the organization cannot
perform one or more of its primary functions, if there’s major damage to
organizational assets, or major financial loss, or serious threat to the
reputation of the company, the expected impact is indeed high.

## Step up your training program

We have covered the basics of the human-as-a-security-sensor paradigm.
You may be interested in integrating employees' reports into existing
security analytics solutions. If that is the case, check out Vielberth
et al.'s
[paper](https://cybersecurity.springeropen.com/articles/10.1186/s42400-019-0040-0).
Anyway, remember: The reports may only be as good as your event
reporting plan, your risk management plan and your training program.
They need to cover the broader social engineering threat landscape. It
is also
[advised](https://www.proofpoint.com/sites/default/files/threat-reports/pfpt-us-tr-state-of-the-phish-2021.pdf)
to go "beyond the phish" by considering risks (e.g., insider threats),
physical security measures and best practices for remote working.

Even though some experts
[argue](https://threatpost.com/cybersecurity-failing-ransomware/175637/)
that user error will always be a thing, it doesn’t hurt to raise
security awareness and promote better quality and quantity of user
reports. After all, your employees are your closest security allies.
