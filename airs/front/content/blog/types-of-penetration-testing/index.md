---
slug: types-of-penetration-testing/
title: Types of Penetration Testing
date: 2023-01-17
subtitle: Pentesting is a system-agnostic approach to security
category: philosophy
tags: pentesting, security-testing, hacking, social-engineering, company, cybersecurity
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1673965755/blog/types-of-penetration-testing/cover_pentesting.webp
alt: Photo by Thomas Griggs on Unsplash
description: The types of penetration testing include external and internal network, wireless, IoT, mobile application and social engineering pentesting. Learn more here.
keywords: Types Of Penetration Testing, Network Penetration Testing, Web Application Penetration Testing, External Penetration Testing, Application Penetration Testing, Internal Penetration Testing, Mobile Application Penetration Testing, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/xsGApcVbojU
---

[Penetration testing](../what-is-manual-penetration-testing/)
(aka "manual" penetration testing)
is a well-known cybersecurity testing approach
that leverages the expertise of ethical hackers,
or penetration testers,
to find complex weaknesses and vulnerabilities.
It is commonly classified into different types,
which refer to the assessments' target information system.
These technologies differ somewhat in the kinds of issues
they tend to have
and the techniques attackers use to discover them.
However,
penetration testing steps or phases across types are usually the same:
planning, reconnaissance, vulnerability assessment, exploitation and reporting.
Learn about these types,
which we cover in our [Penetration Testing solution](../../solutions/penetration-testing/).

## External penetration testing

This type of network penetration testing focuses on the security
of Internet-facing systems.
The controls that guard technology such as websites,
databases,
web applications
and File Transfer Protocol servers
are what you may have heard of as an organization's "perimeter security."
The goal of external network penetration testing
is finding weaknesses in these controls
as well as vulnerabilities in the systems themselves.

This type of testing is quite valuable
because it involves the simulation of external attackers
to see if the network can be breached,
which is necessary
as organizations have an increasing Internet presence.
From this perspective,
the offensive techniques used by ethical hackers include
vulnerability scanning,
information gathering,
brute force (e.g., password spraying, credential stuffing)
and exploitation.
Given the constant evolution of cyber threats,
organizations are advised to request tests to every system
(e.g., web application penetration testing,
cloud penetration testing)
continuously (i.e., **all the time**).

When pen testers probing the network from the exterior
are not given detailed information
nor access to source code prior to the assessments,
this is considered a type of black-box penetration testing.
Although throughout this writing it will be apparent
that any pentesting engagement could also be of the white-box type,
which gives initial access to source code,
or gray-box type,
which gives limited initial information.
(These categories are beyond the scope of this post,
as the criterion from which they arise is the information initially available,
not the kind of system under assessment).

## Internal penetration testing

In contrast to the previous type of pentesting,
this one simulates the ways an adversarial threat actor behaves
after having gained access to the internal network.
Importantly,
these assessments can give insight
into the ways an insider could intentionally
or unintentionally expose the organization to risks.

Among the techniques ethical hackers may use in internal penetration testing
are adversary-in-the-middle attacks
(e.g., Link-Local Multicast Name Resolution (LLMNR) poisoning),
stealing or forging Kerberos tickets,
and IPv6 attacks.

[Read here](../../systems/networks-and-hosts/)
about how we assess networks continuously
with external and internal penetration testing.

## Wireless penetration testing

Organizations can leverage pen testing
to assess whether attackers can compromise their Wi-Fi
and access their network.
The search for vulnerabilities often involves assessing access points,
wireless clients
and wireless network protocols (e.g., Bluetooth, LoRa, Sigfox).
Common findings are weaknesses in encryption
and Wi-Fi Protected Access (WPA) key vulnerabilities.
The techniques ethical hackers may use include brute force,
compromising wireless devices
and deploying rogue access points within the network.

<cta-banner
  buttontxt="Read more"
  link="/solutions/penetration-testing/"
  title="Get started with Fluid Attacks' Penetration Testing solution
  right now"
/>

## IoT penetration testing

The Internet of Things (IoT) is a system
that involves the interaction of plenty of different conventional assets
(e.g., cloud services, operating systems, applications)
with the various smart devices connected to the same network.
In this case,
additional effort is required to control possible attack vectors.
These are different from those of the traditional IT infrastructure,
since compromising any of the devices or sensors in the IoT
can mean compromising the whole IoT infrastructure.
Pentesting is used to gain insight on how resistant the corporate IoT is
against external adversarial threats.

In penetration testing,
ethical hackers might do physical inspections of IoT devices
additionally to their network reconnaissance.
Moreover,
they may conduct firmware analysis,
including assessing third-party libraries
and encryption and obfuscation techniques.
Therefore,
penetration tests are useful
to find issues such as out-of-date firmware misconfigurations
and insecure protocols and communication channels.

[Check out here](../../systems/iot/)
how we help keep the IoT free from security weaknesses and vulnerabilities.

## Mobile application penetration testing

As phones become ever so present in organizations
to fulfill business operations,
the security of the apps downloaded to them is a necessity.
Penetration testing is used to find complex security issues,
like business logic, deployment configuration and injection flaws
in apps running on operating systems such as Android, iOS and Windows UI.
Such manual work
in combination with automation (vulnerability scanning)
increases the accuracy of the security assessments,
yielding low rates of false positives and false negatives.

For this type of testing,
ethical hackers may manually review source code,
develop custom exploits
and even conduct reverse engineering
to check whether the assessed mobile apps lack effective mechanisms
to obfuscate code and prevent information disclosure.
The processes of reviewing code and attack the app as it runs correspond,
respectively,
to [static application security testing](../../categories/sast/) (SAST)
and [dynamic application security testing](../../categories/dast/) (DAST).
We have defined mobile application security testing (MAST),
as well as mentioned a list of top risks to mobile apps
in [another blog post](../what-is-mast/).

[Learn here](../../systems/mobile-apps/)
how we help secure mobile applications continuously.

## Social engineering penetration testing

A broad definition of "information system" includes people.
Indeed,
humans collect, process, store and distribute information
vital to the operations of organizations.
In view of this,
cybersecurity is interested in people
as actors who can prevent cyberattacks.
Penetration testing enters this scenario
as an approach to assess organizations' resistance to attacks
through its personnel.

The way in which persons are attacked is [social engineering](../social-engineering/).
This is when attackers try to influence persons
into taking cybersecurity risks.
You've probably heard of [phishing](../phishing/),
where adversaries send messages to target organizations' employees
persuading them to follow fraudulent web routes,
open attachments
or send a response.
This and similar techniques
(e.g., phone-based scams)
can be used in penetration testing,
of course,
without the prior knowledge of the people
whom the ethical hackers are attempting to scam.
Identifying weaknesses in their responses
helps pinpoint areas of the human element of cybersecurity
that need strengthening with training
(e.g., identifying phishing messages,
[detecting and reporting](../human-security-sensor/) unusual behavior).

At Fluid Attacks,
we provide testing with social engineering techniques
in our [Red Teaming solution](../../solutions/red-teaming/).

## Penetration testing with Fluid Attacks

Fluid Attacks conducts [continuous penetration testing](../../solutions/penetration-testing/)
throughout the software development lifecycle (SDLC).
In this blog post,
we provided links to pages
that expand on how we cover with our solution
the types most penetration testing companies offer.
If you would like to learn more,
take a look at the [systems we assess](../../systems/).

Remember
that by many standards,
like the [recent changes to regulations](https://www.federalregister.gov/documents/2021/12/09/2021-25736/standards-for-safeguarding-customer-information)
following the Gramm Leach Bliley Act,
or GLBA,
penetration testing must be conducted regularly.
We help you go beyond basic compliance
and help you secure your software continuously as you develop it.
Our service is [Continuous Hacking](../../services/continuous-hacking/),
and its most comprehensive [plan](../../plans/) includes penetration testing.

You can start your [**21-day free trial of Continuous Hacking**](../../free-trial/),
which includes only our automated security testing.
Try it
and upgrade whenever you want
to the plan that includes manual testing.
