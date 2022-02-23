---
id: treatments
title: Treatments
sidebar_label: Treatments
slug: /machine/web/vulnerabilities/management/treatments
---

## Define a treatment for your vulnerabilities

To better manage
all the vulnerabilities of a group,
you can assign a treatment
to each individual one
as soon as they are reported.
In order to do this
click on a vulnerability,
a window will appear
where you can see
detailed information about it
and also a tab called **Treatments**

![Enabled Reattack Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211885/docs/web/vulnerabilities/management/vulnerabilities_treatments_oxzujo.webp)

In this tab
you will be able
to assign a treatment
for the selected vulnerability.
The treatments available to you
for handling vulnerabilities
are the following:

- **In progress:**
  With this treatment
  you acknowledge the existence
  of the vulnerability
  and assign an user to it
  in order to ensure
  it is solved.
- **Temporarily accepted:**
  This treatment is used
  when you don't intend
  to give a solution
  to the vulnerability,
  but only temporarily,
  in which case
  you accept the risks
  that comes with it
  until a selected date.
- **Permanently accepted:**
  As with the previous treatment,
  this is used
  when you don't intend
  to solve the vulnerability,
  but this time
  you accept the risks
  that come with it
  permanently.

You will need to provide
certain additional information
about the vulnerability
and its selected treatment,
this information will differ slightly
depending on which treatment is given:

- **Treatment justification:**
  Here you can state the reasons
  for giving this treatment
  to the selected vulnerability.
- **Tags:**
  Assign a label or labels
  to the vulnerability
  for an easier time
  managing and finding them.
- **Level:**
  You can use this field
  to assign a level of priority
  when solving vulnerabilities.
  It can be a number between
  0 and 1,000,000,000 (one billion)
  that represents the severity
  of the vulnerability
  for the business.
  It can be a quantitative
  or monetary value.
- **Assigned:**
  This will be the user of the group
  in charge of making sure
  that the vulnerability
  receives a solution.
- **Temporarily accepted until:**
  This information is for
  when the treatment given
  is **Temporarily accepted**
  in order to know
  the number of days
  that you accept the risk
  of the vulnerability being open,
  when this time is over
  you will need to set
  the treatment once again.

There is also a special treatment
that you can give
to your vulnerabilities
called **Zero Risk**,
you can get more information
about this treatment
by clicking
[this link](/machine/web/vulnerabilities/management/zero-risk).

## Reattacking a permanently accepted vulnerability

Over time, you may request
a reattack —which is a request
for us to validate the
effectiveness of remediation— on
a vulnerability that has been
permanently accepted.
This may happen, as it is possible
that you may have found a solution
to this vulnerability and would
therefore like our hackers to test
whether or not its implementation
was effective.
Thus, the **permanently accepted**
treatment represents an open
location for which you can request
a reattack on the ASM with no problem.

To request a reattack on a
permanently accepted vulnerability,
you must go to the vulnerability
type, tick the check box on the
left of the location you want to
reattack, and click **Reattack**.

![Request Reattack](https://res.cloudinary.com/fluid-attacks/image/upload/v1645628305/docs/web/vulnerabilities/management/treatment_vuln_type_to_request.png)

A pop-up window will appear asking
you to provide a description of
the solution you applied to this
vulnerability.

![Justification Window](https://res.cloudinary.com/fluid-attacks/image/upload/v1645627612/docs/web/vulnerabilities/management/treatment_just_window.png)

Click **Proceed**, and the description
saying **Reattack: Requested** will
appear in front of the previously
selected location.

![Reattack Requested](https://res.cloudinary.com/fluid-attacks/image/upload/v1645627612/docs/web/vulnerabilities/management/treatment_reattack_requested.png)

For the purpose of traceability, you
can go to the **Consulting** section,
where all the history of reattack
requests, along with their respective
justifications, persons in charge and
submission dates are recorded.

![Consulting Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1645627612/docs/web/vulnerabilities/management/treatment_consulting_sect.png)

A hacker will be responsible for
verifying the effectiveness of the
remediation, with a response deadline
of 16 business hours.
In case the evaluation results show
that the vulnerability is still open,
this means that the hacker found a
way to exploit it.
Evidence of this will be provided
by the hacker.
You can access this evidence by
going to the **Evidence** tab.

![Evidence Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1645627612/docs/web/vulnerabilities/management/treatment_evidence_tab.png)

To know the status of the reattack,
you simply need to go to the
**Locations** tab and see what is
next to **Reattack**.
The **gray** circle with the description
**Requested** will appear at the
beginning when the reattack is about
to be carried out or is in progress.
The **red** circle and the description
**Verified** will appear if the
vulnerability remains open in the
corresponding location after the reattack.
Conversely, the **green** circle and
the description **Verified** will appear
if the vulnerability is closed in the
corresponding location after the reattack.
