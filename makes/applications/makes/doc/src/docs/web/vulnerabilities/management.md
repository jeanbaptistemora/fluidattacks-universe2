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

You will need to provide certain additional information about the
vulnerability and its selected treatment, this information will differ slightly
depending on which treatment is given:

- **Treatment justification:** Here you can state the reasons for giving this
treatment to the selected vulnerability.
- **Tags:** Assign a label or labels to the vulnerability for an easier time
managing and finding them.
- **Level:** You can use this field to assign a level of priority when solving
vulnerabilities.
- **Treatment manager:** This will be the user of the group in charge of making
sure that the vulnerability receives a solution, which means this information
is only given when the treatment assigned is **In progress**.
- **Temporarily accepted until:** This information is for when the treatment given
is **Temporarily accepted** in order to know the number of days that you accept
the risk of the vulnerability being open, when this time is over you will need
to set the treatment once again.

### Zero risk vulnerability

There is a special treatment that you can give to any reported vulnerabilities which
is called **zero risk**, which means that according to analysis and consideration
taken by your organization, this vulnerability poses no threat. In order to make
a Zero Risk request you can take the same steps taken to assign a normal treatment.

![Request Zero Risk](/img/web/vulnerabilities/management/request_zero_risk.png)

After choosing to give a Zero Risk treatment to the selected vulnerability you
only need to add a treatment justification, this information will be used by us
to consider whether the vulnerability actually poses no threat at all, in which
case the vulnerability will be deleted, however, if we still consider there is a risk,
then it will remain reported.

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

## Tracking your vulnerabilities

As time passes and your project changes, it becomes necessary to have an efficient way
of knowing how has a type of vulnerability evolved over time. This can be visualized
in the **Tracking** tab available within each type of vulnerability.

![Vulnerability Tracking Tab](/img/web/vulnerabilities/management/vulnerabilities_tracking.png)

The information than can be seen here will be divided in cycles based on the date
of the change and the type of change that occured. Here you will be able to
visualize the amount of vulnerabilities that were opened/closed in a specific date
and also the treatment that a set amount of vulnerabilities were given in a
specific date, mentioning its justification and treatment manager.
