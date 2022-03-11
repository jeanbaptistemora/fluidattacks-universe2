---
id: treatments
title: Treatments
sidebar_label: Treatments
slug: /machine/web/vulnerabilities/management/treatments
---

## Define a treatment for your vulnerabilities

A treatment is a business decision
that the client makes concerning a
vulnerability.
This decision refers to what the
client wants to do with that vulnerability:
how to address or remediate it.

In order to define a treatment, you
will need to go to either the **Locations**
tab or the **To-Do List** section.
Then, you will need to select the
vulnerability to which you want to
assign a treatment by clicking the
check box to its left and click
on **Edit**.

![Vulnerability Assign](https://res.cloudinary.com/fluid-attacks/image/upload/v1646420467/docs/web/vulnerabilities/management/treatments_vulner_assign_trtmnt.jpg)

The **Edit** button helps you manage
the vulnerability treatments and
is available in the two aforementioned
locations.
After you click on it, a pop-up
window will appear, where you can
assign a **treatment** and provide a
justification for that treatment.
You can also assign the person
responsible for handling this
vulnerability in the field labeled
**Assigned**.
Remember that you can see the
vulnerabilities that have been
assigned to you in the
[To-Do List](/machine/web/vulnerabilities/management/to-do-list)
section.

![Edit Vulnerability](https://res.cloudinary.com/fluid-attacks/image/upload/v1646420467/docs/web/vulnerabilities/management/treatments_edit_vulnerabilities.png)

The treatments available to
you for handling vulnerabilities
are the following:

- **In progress:**
  With this treatment,
  you acknowledge the
  existence of the
  vulnerability and
  assign it to a user.
  This assignment is
  located in the To-Do
  List, where the user
  can be aware of all
  the vulnerabilities
  they are responsible
  for remediating in
  their daily work.
- **Temporarily accepted:**
  This treatment is used
  when you do not intend
  to remediate the
  vulnerability, at least
  for a certain period.
  You accept the risks
  that come with it up to
  a specific date.
  When this time is over,
  you are in charge of
  defining the treatment
  once again.
- **Permanently accepted:**
  As with the previous treatment,
  this is used
  when you don't intend
  to remediate the vulnerability,
  but this time you accept the
  risks that come with it
  permanently.
- **Zero risk:**
  This is a special treatment
  that you can define for a
  vulnerability which,
  according to your
  organization’s analysis,
  poses no threat.
  We will then analyze whether
  that is the case.
  If so, the vulnerability
  will be removed from the list.
  Otherwise, it will remain
  reported.
  You can get more information
  about this treatment under
  [this link](/machine/web/vulnerabilities/management/zero-risk).

You will be asked to provide
additional information about
the vulnerability and the
treatment you defined.
This information will differ
slightly depending on the
treatment:

- **Treatment justification:**
  Here you must state the
  reasons for requesting
  this treatment for the
  selected vulnerability.
- **Tags:**
  You can assign one or
  more labels to the
  vulnerability to make
  it easier to manage
  and find them.
- **External BTS:**
  The Bug Tracking System
  (BTS) is a platform for
  issues management and
  tasks tracking that is
  internal for each client.
  In this field, you can
  provide the URL of the
  issue concerning this
  vulnerability.
- **Level:**
  You can use this field
  to assign a level of
  priority when remediating
  vulnerabilities.
  It can be a number between
  0 and 1,000,000,000 that
  represents the severity
  of the vulnerability for
  the business.
  It can also be a monetary
  value.

Keep in mind that the **User**
role can define the
Temporarily accepted,
In progress and Zero
risk treatments.
They can also suggest treating
a vulnerability as **Permanently accepted**,
but the only roles that can
approve it are either the **user manager**
or the **vulnerability manager**.

![Confirmation](https://res.cloudinary.com/fluid-attacks/image/upload/v1646420467/docs/web/vulnerabilities/management/treatments_confirmation.png)

Both the user manager or the
vulnerability manager can
either approve or reject a
**Permanently accepted** treatment
request.
To do this,
they need to select a
vulnerability and click on the
**Treatment Acceptance** button,
which is only available to them.

![Treatment Acceptance](https://res.cloudinary.com/fluid-attacks/image/upload/v1646420467/docs/web/vulnerabilities/management/treatments_tr_acceptance.jpg)

A pop-up **Observations**
window will appear,
where the user manager or the vulnerability
manager must provide their
observation concerning the requested
treatment and decide whether
they approve or reject it.

![Observations](https://res.cloudinary.com/fluid-attacks/image/upload/v1646420467/docs/web/vulnerabilities/management/treatments_pop_up_observations.png)

If the treatment is approved,
the vulnerability status will
immediately change to
**Permanently accepted**.
Otherwise,
the status will appear as
**In progress**.

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
