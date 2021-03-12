---
id: vulnerabilities
title: Vulnerabilities
sidebar_label: Vulnerabilities
slug: /web/groups/vulnerabilities
---

The tab of **Vulnerabilities** is the first one you will see when clicking on a
group, in this tab you will find a table listing all of the vulnerabilities
for the group and also the **Reports** button, which can be used to request one
of the several types of reports about all the vulnerabilities the group has.

## Table of vulnerabilities

In this table you will find the vulnerabilities categorized by their **type** and
you can organize them by clicking on the various columns that will be described here

![Vulnerability Table First Half](/img/vulns_table_1h.png)

- **Age(days):** This column shows the amount of days passed since that specific
type of vulnerability was first found.
- **Open Age(days):** This is the amount of days passed since the oldest of all the
open vulnerabilities was found, thus, if the vulnerability is closed, this number
will be 0.
- **Last report(days):** The amount of days passed since a vulnerability of this
specific type was found, regardless of its open/closed status.
- **Type:** Depending on several characteristics of a single vulnerability, we can
categorize them in various groups. This column represents such categorization.
- **Description:** A brief explanation about what this type of vulnerability does.
- **Severity:** This is the score given to each type of vulnerability. We use the
[CVSS](/web/glossary/#cvss "Common Vulnerability Scoring System") standard to assign
each score.

![Vulnerability Table Second Half](/img/vulns_table_2h.png)

- **Open:** This column shows the amount of vulnerabilities that currently haven't
been resolved.
- **Status:** This column tells you that it is Open if there is at least one
vulnerability that hasn't been resolved yet, otherwise it will tell you it is
Closed.
- **Treatment:** This column will show you the treatments that can be given to a
vulnerability and a number in front of them. This number corresponds to the
amount of vulnerabilities that are receiving the corresponding treatment.
- **Verification:** This column shows you if there is at least one vulnerability
that is still in the process of being reattacked for verification.
- **Exploitable:** This column will tell you, according to the score given to
the specific type, if the vulnerability can be exploited or not.
- **Where:** This column shows you a number of specific locations of the
vulnerabilities, however if there are too many of the same type, you will need
to click on it and access the **Location** tab of the vulnerability to see
all of them.

## Reports

In the vulnerabilities tab, you can also request several reports about the
vulnerabilities by clicking the **Reports** button seen in the following image

![Reports Button](/img/reports_button.png)

When you click on it, the following window will show up

![Reports Modal](/img/reports_modal.png)

There are three types of report you can request:

- **Executive:** This will give you a more summarized report of all the
vulnerabilities in line with the knowledge needed from a managerial
perspective.
- **Technical:** This report will give a much more in-depth look at all the
vulnerabilities of the group, suitable for those that want all the
technical details.
- **Export:** This option will give you a zip file with an export of all
the vulnerabilities of the group.

Lastly, as you can see in the image, in order to download the report you need
to check your e-mail and click on the **Download** button you can see in the
following image

![Reports Mail](/img/reports_mail.png)

The downloaded file will be protected with a passphrase which will be sent to
your mobile device. You can check the documentation for our
[mobile app](/web/groups/vulnerabilities#reports) in case you encounter any
trouble in this part of the process.
