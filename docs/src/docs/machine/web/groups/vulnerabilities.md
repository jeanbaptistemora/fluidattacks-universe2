---
id: vulnerabilities
title: Vulnerabilities
sidebar_label: Vulnerabilities
slug: /machine/web/groups/vulnerabilities
---

The tab of **Vulnerabilities** is the first one
you will see
when clicking on a group.
In this tab,
you will find a table
listing all the vulnerabilities in the group
and the **Reports** button,
which you can use
to request one of several types of reports
on all the vulnerabilities present there.

## Table of vulnerabilities

In this table,
you will find the vulnerabilities
categorized by their **type**
and you can organize them
by clicking on the various columns
described here:

![Vulnerability Table First Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211894/docs/web/groups/vulnerabilities/vulns_table_1h_m2j4au.webp)

- **Age (days):**
  The number of days elapsed
  since we first identified
  that specific type of vulnerability.
- **Open age (days):**
  The number of days passed
  since the oldest
  of all the open vulnerabilities
  was found,
  thus,
  if the vulnerability is closed,
  this number will be 0.
- **Last report (days):**
  The number of days passed
  since we found a vulnerability
  of that specific type,
  regardless of its open/closed status.
- **Type:**
  Depending on several characteristics
  of a single vulnerability,
  we can categorize them
  into various groups.
  This column represents
  such categorization.
- **Description:**
  A brief explanation
  of what that type of vulnerability does.
- **Severity:**
  This is the score given
  to that type of vulnerability.
  We use the CVSS
  (Common Vulnerability Scoring System)
  standard to assign each score.

![Vulnerability Table Second Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211894/docs/web/groups/vulnerabilities/vulns_table_2h_s8mag6.webp)

- **Open:**
  This column shows the number of vulnerabilities
  that have not been resolved.
- **Status:**
  This column tells you "Open"
  if at least one vulnerability
  has not yet been resolved;
  otherwise,
  it will tell you "Closed."
- **Treatment:**
  This column shows you the treatments
  that can be given
  to a vulnerability.
  Each treatment has a number in front of it
  That represents the number of vulnerabilities
  receiving it.
- **Verification:**
  This column shows you
  if there is at least one vulnerability
  that is still in the process
  of being reattacked for verification.
- **Exploitable:**
  This column tells you
  whether the vulnerability can be exploited
  or not
  according to the score given
  to the specific type.
- **Where:**
  This column shows you
  several specific locations of vulnerabilities.
  However,
  if there are too many vulnerabilities
  of the same type,
  you should click on it
  and access the **Location** tab
  to see them all.

## Reports

In the Vulnerabilities tab,
you can also request
various vulnerability reports
by clicking on the **Reports** button
shown in the following image:

![Reports Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211894/docs/web/groups/vulnerabilities/reports_button_yzszmw.webp)

When you click on it,
the following window will appear:

![Reports Modal](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211894/docs/web/groups/vulnerabilities/reports_modal_h26dmp.webp)

There are three types of reports
you can request:

- **Executive:**
  This will give you a more summary report
  of all vulnerabilities
  in line with necessary knowledge
  from a management perspective.
- **Technical:**
  This will give a much more in-depth look
  at all the group's vulnerabilities,
  being suitable for those
  that want all the technical details.
- **Export:**
  This will give you a zip file
  with an export of all vulnerabilities
  in the group.

Lastly,
in order to download the report,
you need to check your email
and click on the **Download** button
that you can see in the following image:

![Reports Mail](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211894/docs/web/groups/vulnerabilities/reports_mail_zjkigl.webp)

The downloaded file will be protected
with a passphrase
that we will send
to your mobile device.
You can refer
to our [mobile app documentation](/machine/web/groups/vulnerabilities#reports)
if you encounter any problems
with this part of the process.
