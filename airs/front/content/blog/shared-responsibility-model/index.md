---
slug: shared-responsibility-model/
title: Security Breaches Are Your Fault!
date: 2021-03-05
subtitle: Confusion with the cloud shared responsibility model
category: philosophy
tags: cloud, information, cybersecurity, security, mistake, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331096/blog/shared-responsibility-model/cover_musv3h.webp
alt: Photo by Charles Deluvio on Unsplash
description: Do you know what is happening with those who don't understand
  the cloud security shared responsibility model? Find out here and get
  some recommendations.
keywords: Cloud, Security, Shared Responsibility Model, SRM, CSP, Confusion,
  Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/K4mSJ7kc0As
---

[In a previous post from late 2019](../security-trends/), Oscar Prado,
cybersecurity analyst at `Fluid Attacks`, touched on the matter of most
companies migrating to the cloud. [One year
later](../cybersecurity-2020-21-i/), we indicated a substantial
acceleration and growth in that phenomenon, primarily driven by the
pandemic and the security measures that emerged as necessary,
particularly remote work. It’s true that hosting a business in the cloud
offers significant benefits in terms of cost, speed, scalability,
maintenance, among others. Nevertheless, there are often issues
concerning the security of companies' systems and assets in the cloud,
mostly due to a lack of knowledge and confusion about something known as
the security shared responsibility model (SRM). Let’s see what’s
happening.

## What is cloud computing?

As [Ranger said on
ZDNet](https://www.zdnet.com/article/what-is-cloud-computing-everything-you-need-to-know-about-the-cloud/),
"Cloud computing is the delivery of on-demand computing services —from
applications to storage and processing power— typically over the
internet and on a pay-as-you-go basis." So now, [for
example](https://medium.com/@aditi.chaudhry92/what-is-cloud-computing-59d0d5570332),
if you intend to develop and offer a new application, you don’t have to
do as before, gradually acquiring software and hardware resources and
maintaining your own computing infrastructure. You can save money, time,
and effort by paying for web-based services according to your needs. The
clouds of companies like Amazon, Microsoft, and Google have incredible
amounts of resources pooled in their infrastructures for your benefit
while your projects are hosted there. Thus, as its fame grows, for
instance, your application can quickly increase its use of cloud servers
to satisfy your customers with speed and effectiveness. Yet, it can also
easily reduce cloud usage if its popularity ever declines. You then pay
strictly for what you need at a specific time.

"Rarely do people mention how security is a benefit of moving to the
cloud," [said
Chaudhry](https://medium.com/@aditi.chaudhry92/how-to-be-secure-in-the-cloud-613846412db1)
more than two years ago. But why? Indeed, leading cloud service
providers (CSPs; [AWS is the top
cloud](https://www.zdnet.com/article/cloud-computing-aws-is-still-the-biggest-player-but-microsoft-azure-and-google-cloud-are-growing-fast/),
although Microsoft Azure and Google Cloud are growing fast) may possess
more experienced and skilled cybersecurity staff than many other
companies could ever hire. There’s no doubt that a business working
within a cloud has significant benefits in terms of security. However,
unknown to many, these are only partial benefits.

## What is the SRM?

According to [Violino on
CSO](https://www.csoonline.com/article/3043030/top-cloud-security-threats.html),
for example, "Contrary to what many might think, the main responsibility
for protecting corporate data in the cloud lies not with the service
provider but with the cloud customer." Cloud security efforts don’t
depend on just one of the parties involved. In fact, [CSPs subscribe to
the globally accepted security
SRM](https://blog.radware.com/security/cloudsecurity/2020/10/understanding-the-shared-responsibility-model/),
in which they are primarily concerned with the security of physical
aspects, infrastructure, network, and virtualization. On the other hand,
the customer must always guarantee the security of the user
access/identity and data. As shown in **Figure 1**, the party
responsible for protecting the application or the guest OS will vary
based on the type of cloud service (IaaS, PaaS, and SaaS; see **Figure
2**). Besides, some other differences in these delimitations may be the
product of the CSPs' particular choices.

<div class="imgblock">

![Oracle](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331095/blog/shared-responsibility-model/oracle_tleunv.webp)

<div class="title">

Figure 1. Cloud security shared responsibility model (source:
[Oracle.com](https://www.oracle.com/a/ocom/docs/cloud/oracle-ctr-2020-shared-responsibility.pdf)).

</div>

</div>

<div class="imgblock">

![IPSaaS](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331094/blog/shared-responsibility-model/ipsaas_jzdvv4.webp)

<div class="title">

Figure 2. Types of cloud services (source:
[Medium.com](https://miro.medium.com/max/2800/1*hlMABmD_hJmMJlu433KIAg.png);
see also [Ranger’s
post](https://www.zdnet.com/article/what-is-cloud-computing-everything-you-need-to-know-about-the-cloud/).

</div>

</div>

In research published in 2020, [Oracle and
KPMG](https://www.oracle.com/a/ocom/docs/cloud/oracle-ctr-2020-shared-responsibility.pdf)
surveyed cloud service subscribers' understanding of SRM. Almost all of
their respondents revealed high levels of familiarity with the term SRM.
However, only **8%** of them said they entirely understand the SRM for
every kind of cloud service. The confusion arising from this variable
distribution of responsibilities in security matters has led many
organizations to overlook several of their obligations inside the cloud
or fail to fulfill them adequately. [One of the most prevalent
implications](https://www.secureworldexpo.com/industry-news/4-types-cloud-security-vulnerability-mitigation)
of such confusion is the misconfiguration vulnerability (which may also
be related to a lack of training).

## What are these cloud security issues?

A widely known case of misconfiguration was the [Capital One data
breach](https://edition.cnn.com/2019/07/29/business/capital-one-data-breach/index.html)
in 2019. According to the SRM, a client company’s employees are
responsible for the appropriate integration of cloud service platforms.
Following [Graham’s
point](https://www.bitsight.com/blog/what-companies-using-cloud-computing-providers-need-to-know-about-their-risk-responsibilities),
"Engineers that have worked with cloud computing systems have frequently
noted that system integrations are [not always
straightforward](https://www.wsj.com/articles/human-error-often-the-culprit-in-cloud-data-breaches-11566898203)."
Either because of confusion, incompetence, or both, Capital One
personnel left a firewall improperly configured in the process of
integrating AWS solutions, allowing the theft of information from more
than **100 million** credit card customers. In conclusion, Capital One,
not AWS, ["was held
accountable](https://www.bitsight.com/blog/what-companies-using-cloud-computing-providers-need-to-know-about-their-risk-responsibilities)
for the monetary loss and time spent fixing the error."

'Data breaches' along with 'Misconfiguration and inadequate change
control' are the first two cloud threats that the [Cloud Security
Alliance (CSA)](https://cloudsecurityalliance.org/) puts on its [Top
Threats to Cloud Computing: Egregious
Eleven](https://cloudsecurityalliance.org/artifacts/top-threats-egregious-11-deep-dive/)
report for the education of organizations. Companies should not only
worry about the risk of losing data or intellectual property but also
about the risk of their cloud resources being deleted or modified to
disrupt business operations. [Confusion with cloud
responsibilities](https://www.oracle.com/a/ocom/docs/cloud/oracle-ctr-2020-shared-responsibility.pdf)
can also lead to errors involving unauthorized access to data and
services. Plus, it can open the door to malware and facilitate the
stealing of cloud credentials.

As [Nunnikhoven told
SecureWorld](https://www.secureworldexpo.com/industry-news/biggest-cloud-security-threat-2021),
the vast majority of cloud service-related incidents have involved
problems on the customer side, not the CSP side. [Apparently, from
Gartner](https://blog.radware.com/security/cloudsecurity/2020/10/understanding-the-shared-responsibility-model/),
it’s expected that by next year, "at least 95% of cloud security
failures will be the customer’s fault." Still, [it’s said
that](https://www.threatscape.com/what-is-the-shared-responsibility-model-your-cloud-security-responsibilities-defined/)
many companies refrain from migrating to the cloud because they perceive
considerable security risks. That’s silly. (Although we should never
rule out the [possibility of
catastrophe](https://www.csoonline.com/article/3573371/cloud-technology-great-for-security-but-poses-systemic-risks-according-to-new-report.html)
in the security of CSPs.) According to the above, they could recognize
that security is an issue that will be primarily affected by their
decisions and actions in both on-premise and cloud infrastructures. But
this is something that even multiple companies inside the cloud haven’t
figured out.

## Recommendations to overcome confusion?

A solution to this problem around the SRM for any company could start
with an education geared towards a cultural shift in which all parties
involved, all teams, discuss cybersecurity. (Remember, [everyone is
responsible for 'Sec'](../devsecops-concept/) if you are following the
DevSecOps approach.) Understanding what the cloud is and which security
requirements are under your responsibility is of vital importance prior
to business migration. (If you are already in the cloud, make sure you
understand this). Keep in mind that it’s never prudent to let a desire
for rapid migration to the cloud take precedence over security. Don’t
let cyber-criminals be the ones to make you and your colleagues aware of
your security obligations with their misdeeds.

Of course, without hesitation, establish a conversation with your CSP
whenever necessary. Ask them for detailed guidelines on your security
responsibilities because they can certainly give them to you. Also, stay
informed of updates to those responsibilities since they may be
evolving. Bear in mind that it’s always crucial to have robust
authentication mechanisms and manage a definite restriction of access to
critical data and systems. Likewise, keep threat models up to date and
deploy continuous monitoring for configuration errors and
vulnerabilities. ([`Fluid Attacks` red
team](../../services/continuous-hacking/) can help you with that.)
Finally, don’t forget that if you don’t understand and address cloud
security in your company’s digital transformation, the next
cybersecurity breach could be your fault\!
