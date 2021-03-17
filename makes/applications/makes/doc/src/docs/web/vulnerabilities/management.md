---
id: management
title: Management
sidebar_label: Management
slug: /web/vulnerabilities/management
---

With Fluid Attacks ASM you will be able to visualize all the details you
need about your reported vulnerabilities and manage them effectively.
Upon clicking on one type of vulnerability in the Vulnerabilities tab of your
group, you will be greeted by a list with all the vulnerabilities of that type.

![Enabled Reattack Button](/img/web/vulnerabilities/management/vulnerabilities_location.png)

At a glance you will be able to tell **Where** in the
[ToE](/web/glossary/#toe "Target of Evaluation") is the vulnerability along with
a more specific location, check if said vulnerability is open or closed, and also
confirm what kind of treatment it is being given.

Besides this there are other useful functionalities you can do here that
enable efficient management of your vulnerabilities:
- Define a treatment for each vulnerability
- Request that a vulnerability be reattacked
- Request a zero risk treatment for a vulnerability
- Check what information was compromised by this type of vulnerability,
if applicable
- Look at a script that replicates the exploitation process of the vulnerability,
if applicable
- Look at a timeline that describes how this type of vulnerability has evolved over time

## Define a treatment for your vulnerabilities

To better manage all the vulnerabilities of a group, you can assign a treatment
to each individual one as soon as they are reported. In order to do this click
on a vulnerability, a window will appear where you can see detailed information
about it and also a tab called **Treatments**

![Enabled Reattack Button](/img/web/vulnerabilities/management/vulnerabilities_treatments.png)

In this tab you will be able to assign a treatment for the selected vulnerability.
The treatments available to you for handling vulnerabilities are the following:

- **In progress:** With this treatment you acknowledge the existence of the
vulnerability and assign a treatment manager to it in order to ensure
it is solved.
- **Temporarily accepted:** This treatment is used when you don't intend to
give a solution to the vulnerability, but only temporarily, in which case
you accept the risks that comes with it until a selected date.
- **Eternally acepted:** As with the previous treatment, this is used when
you don't intend to solve the vulnerability, but this time you accept the
risks that come with it eternally.

## Zero risk vulnerability

Explanation for the process of requesting zero risks.

## Request reattack

When you have applied a solution for an existing vulnerability, you can request a
reattack for us to validate this. This can be done by clicking on the Reattack
button

![Enabled Reattack Button](/img/web/vulnerabilities/management/reattack_button_enabled.png)

The button will deactivate until you select the vulnerabilities you want to reattack

![Disabled Reattack Button](/img/web/vulnerabilities/management/reattack_button_disabled.png)

After selecting one or more vulnerabilities you can click on the Reattack button again,
or you can click on Cancel to dismiss the process.

![Reattack vulnerabilities selected](/img/web/vulnerabilities/management/reattack_vulnselect.png)

The following form will appear, you can explain the solution applied and click on Proceed
to finish the request or Cancel to dismiss it.

![Reattack Request Form](/img/web/vulnerabilities/management/reattack_form.png)

When you finish requesting the reattack, our analysts will verify that the vulnerability
was indeed solved and close or keep it open depending on the verification result.

## Explain Records

Explain the Records tab.

## Explain Exploit

Explain the Exploit tab.

## Explain Tracking

Explain the Tracking tab.
