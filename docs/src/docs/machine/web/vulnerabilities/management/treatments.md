---
id: treatments
title: Treatments
sidebar_label: Treatments
slug: /machine/web/vulnerabilities/treatments
---

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

## Zero risk vulnerability

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
