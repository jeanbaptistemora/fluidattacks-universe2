---
id: reports
title: Reports
sidebar_label: Reports
slug: /machine/web/groups/reports
---

In the
[Vulnerabilities](/machine/web/groups/vulnerabilities)
section,
you can request vulnerability
reports by clicking on the
**Reports** button that
appears at the top left,
as you can see in the
following screenshot:

![Vulnerabilities Subsection](https://res.cloudinary.com/fluid-attacks/image/upload/v1671651481/docs/web/groups/reports/reports.png)

The available report options
have either summarized and
easy-to-read information or
complete and technical
information about the
vulnerabilities that have
been reported in a specific group.
When you click on
the Reports button,
you can see the following
options:

![Reports Options](https://res.cloudinary.com/fluid-attacks/image/upload/v1662054348/docs/web/groups/reports/report_options.png)

- **Certificate:**
  This option generates
  a security testing
  certification.
- **Executive:**
  This option creates a
  summarized report in PDF
  of all vulnerabilities
  reported in the group,
  tailored to a management
  perspective.
- **Technical:**
  This option generates a
  much more in-depth report
  in XLSX of all vulnerabilities
  reported in the group,
  or filtered by treatment,
  suitable for those who want
  all the technical details.
- **Export:**
  This option creates a ZIP
  file with an export of all
  vulnerabilities reported
  in the group (includes the
  previous reports and files
  of compromised records
  and evidence).

When you select the
desired report option,
if you have not yet registered
your mobile phone
number in the ARM,
you will see a message
asking you to do so.
You just have to go to the
[user information drop-down menu](/machine/web/user)
and select the Mobile option.
A verification code will
be sent via SMS to the
number you provide.
Once you have
registered your number,
in order to obtain
the requested report,
you must enter another
verification code that
will be sent to your mobile,
as you can see below:

![Verification Code](https://res.cloudinary.com/fluid-attacks/image/upload/v1662054348/docs/web/groups/reports/report_verification.png)

As immediately announced
by a message in the ARM,
it will send you an email
with a link to the report
in a couple of minutes.
Once you receive it,
clicking on the
**Go to report** button
will allow you to download
the report to your device.
It is essential to note
that the access granted
through the link is only
available for one hour.

![Message](https://res.cloudinary.com/fluid-attacks/image/upload/v1667342446/docs/web/groups/reports/technical_report.png)

## Definitions of Technical report columns

- **Related Finding:**
   [Vulnerability type](/criteria/vulnerabilities/)
- **Finding Id:**
  Vulnerability identifier composed
  by random numbers and letters.
- **Vulnerability Id:**
  Location identifier composed by
  random numbers and letters.
- **Where:**
  Location of the vulnerability
  found with the specific path
  where it is located.
- **Stream:**
  Steps to reach the vulnerability
  in dynamic environments.
- **Specific:**
  Indicates exactly where the
  vulnerability was found
  (line, field or port).
- **Description:**
  Vulnerability description.
- **Status:**
  Vulnerability status can be
  safe or vulnerable.
- **Severity:**
  Vulnerability score based on CVSS
  3.1 standard.
- **Requirements:**
  Unfulfilled [Requirement(s)](/criteria/requirements/)
  based on security standards.
- **Impact:**
  How your application is affected by
  related vulnerability.
- **Threat:**
  How the attacker can exploit the system.
- **Recommendation:**
  Suggestions that can be applied
  to fix related vulnerability.
- **External BTS:**
  Customer Bug Tracking System URL
  used to fix the vulnerability.
- **Compromised Attributes:**
  Data or information that was
  compromised as a result of
  exploiting the vulnerability.
  **Example:** Users, IDs, passwords.
- **Tags:**
  Tag to identify the vulnerability.
- **Business Critically:**
  Numerical value to classify the
  severity of vulnerabilities
  defined by customers for
  their internal use.
- **Type:**
  The location where the vulnerability
  was found.
  Possible values:
  app,
  code,
  infra.
- **Report Moment:**
  Vulnerability confirmation date.
- **Close Moment:**
  Vulnerability fixing date.
- **Age in days:**
  Days have passed since the
  vulnerability was confirmed.
- **First Treatment:**
  First confirmed treatment defined
  to the vulnerability.
- **First Treatment Moment:**
  Date on which the treatment was defined.
- **First Treatment Justification:**
  Treatment applied justification.
- **First Treatment expiration Moment:**
  For [Temporal treatments](/machine/web/vulnerabilities/management/treatments),
  this date shows the date which
  treatment expires.
- **First Assigned:**
  Who was the first person to be
  assigned this vulnerability.
- **Current Treatment:**
  The current treatment of the vulnerability.
- **Current Treatment Moment:**
  Date on which current treatment was applied.
- **Current Treatment Justification:**
  Justification for applying current treatment.
- **Current Treatment expiration Moment:**
  Expiration date for  current treatment.
- **Current Assigned:**
  The name of the person who is
  currently assigned to the vulnerability.
- **Pending Reattack:**
  Whether they have requested a reattack or not.
- **# Requested Reattacks:**
  The total number of times reattacks
  have been requested.
- **Remediation Effectiveness:**
  The effectiveness percentage of the
  remediation of that vulnerability.
- **Last requested reattack:**
  The date on which the most recent
  reattachment was requested.
- **Last reattack Requester:**
  Email of the user who requested
  the most recent reattack.
- **CVSSv3.1 string vector,**
   **Attack Vector,**
   **Attack Complexity,**
   **Privileges Required,**
   **User Interaction,**
   **Severity Scope,**
   **Confidentiality Impact,**
   **Integrity Impact,**
   **Availability Impact,**
   **Exploitability,**
   **Remediation Level and**
   **Report Confidence:**
  All these columns are part
  of the Severity Score
  [CVSS](https://www.first.org/cvss/v3.1/specification-document)
  values.
- **Commit Hash:**
  Commit identifier where the
  vulnerability was found.
- **Root Nickname:**
  The nickname of that root
  where the vulnerability was found.

## Report Filters

If you want to customize
the technical report,
you have the option to
apply filters to these
reports to generate the
data you are interested in.
To use these,
you must go to the filters
button on the right side of
the Technical Report button.

![Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1657731874/docs/web/groups/reports/reports_filters.png)

When you click on it,
a pop-up window will appear
where you will be able to
select what information
you want to generate,
finding four different
filter options:

![Filter Options](https://res.cloudinary.com/fluid-attacks/image/upload/v1667385312/docs/web/groups/reports/filters_report.png)

- **Type:**
  Filter by the name of vulnerability
  type.
- **Min release date:**
  Filter the vulnerabilities with the
  most recent date when the
  vulnerability was reported.
- **Max release date:**
  Filter vulnerabilities with
  the oldest date it was reported.
- **Locations:**
  The localization of vulnerability.
- **Last Report:**
  Filter types by days since the
  last reported vulnerability.
- **Min - Max severity:**
  Filter out vulnerabilities with
  min and max severity value.
- **Age:**
  Filter the typology according
  to the age it has.
- **Closing date:**
  Filters closed locations
  with a date equal to or
  before the specified date.
- **Treatment:**
  Filter locations according
  to treatment.
- **Reattack:**
  Filter locations according
  to their Reattack status.
- **Status:**
  Filter vulnerabilities
  according to Open/Closed state.

When you apply the
filters of your interest,
click on the generate XLS button.
You will receive the verification
code on your cell phone;
after successful verification,
you will receive the report in
your email with the selected data.
