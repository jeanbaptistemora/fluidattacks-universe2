---
id: speed
title: Speed
sidebar_label: Speed
slug: /about/faq/speed
---

## When does Squad Plan hacking begin?

It begins immediately
after receiving the purchase order.

## How is a project's progress determined?

A project's progress and current status
are determined using the following metrics:

- Source code coverage indicator
- Percentage of remediated security risk vulnerabilities

## Does the Squad Plan use automated tools or is it a manual process?

Automated tools
alone
are not capable of extracting sensitive business information,
such as that of clients or employees.
In our Squad Plan service,
we use a series of tools
acquired and developed by us at `Fluid Attacks`,
as well as a detailed review process
performed by our expert technical staff.
We go the extra mile
because automated tools present the following problems:

- Vulnerability leakages
  (detection of a minimal percentage
  of existing security risk vulnerabilities).

- Detected vulnerabilities
  are primarily false positives.

- Incapability of combining individual vulnerabilities
  in order to reveal additional vulnerabilities
  which may be an even greater security risk
  than the individual vulnerabilities alone.

## How are development cycles not slowed down by manual reviews?

Squad Plan hacking is first performed
on the source code.
This allows for hacking
and development to occur simultaneously,
which minimizes the dependency on functional environments,
as well as the need for coordination
between hackers and developers.
The decisions regarding which findings are prioritized
for each sprint
rest solely with the client.
Unless we are dealing with a company with daily CI/CD
(Continuous Integration/Continuous Deployment),
not all sprints generate code
eligible for release and deployment,
which improves the remediation time
for detected vulnerabilities.

## How can a project develop rapidly with the Squad Plan's manual reviews?

Standard Squad Plan hacking covers **95%**
of all business applications being developed.
Subscription is based on the number of active developers
in the project,
which defines the number of resources allocated.

## How can your manual reviews keep up with a client's big app portfolio?

Based on our historical data,
and thanks to our recruitment
and training capabilities,
as well as our ability
to innovate internal processes,
we are fully capable of taking on between **5** and **10**
new applications each month.

## How long does it take you to review a new commit?

The goal is **100% coverage**.
Therefore,
there will be results
regarding system vulnerabilities
continuously
throughout the contract period.
We take into account all pushes to the tested branch,
which are monitored using automated scripts (robots)
that extract and analyze the changes
made to the source code every night.

## What are the scheduled activities during the Squad Plan test?

Once the setup has been completed
and everything is ready for the service,
the security tests start.
The steps are as follows:

1. Approval request
   (purchase order confirmed).

1. Project leader assignment.

1. The project leader schedules the start meeting
   (teleconference).

1. Service condition validation.

1. Supplies request
   (access to environments and code).

1. The project leader receives supplies
   and programs the setup
   of the verification and access robots.

1. The project leader creates an admin user
   in [ASM](https://fluidattacks.com/categories/asm/)
   (Attack Surface Manager)
   for the client.

1. The admin user invites all project stakeholders,
   including the developers.
   (They must have Google Apps or Office365.)

1. Vulnerabilities are reported in ASM.

1. Project stakeholders access vulnerabilities
   and start remediation.

1. If any questions or problems arise,
   they can be addressed through the comments
   or chat available in ASM.

1. When the client has remediated the reported vulnerabilities,
   they may request validation of their repairs
   through ASM.

1. Our hacker performs the closure verification
   and updates the report.

1. Steps **3 to 7** are repeated
   until the subscription ends.

## Do you test every time I make a push in the subscription branch?

During the execution of a project,
the following scenarios can occur:

- Application in development without overdue code
  (**100% coverage**):
  The robot detects the change
  and generates the updated control files.
  This means
  that no specific file or commit is audited,
  but rather the change analysis
  performed by the robot
  is incorporated
  when the hackers attack the application,
  thus allowing them
  to take into account
  the changes made.

- Application in production without overdue code
  (**100% coverage**):
  Even when there are no changes,
  the application is attacked.
  Internally,
  we have processes
  that help us identify
  why we haven't found vulnerabilities
  in the application
  in 7, 14 and 21 days.
  These processes include such things
  as hacker rotations
  or increasing the number of hackers
  assigned to the project
  in order to find undiscovered vulnerabilities.

- Application in development with overdue code
  (**<100% coverage**):
  Same as the first scenario,
  but attacks are only related to the change
  that was made.
  The attack surface that existed
  before the subscription point
  is not attacked.

- Application in production with overdue code
  (**<100% coverage**):
  Same as the second scenario,
  but if there is no new code
  in a specified month,
  it is hacked only to the extent of the changes made
  by _one_ active author
  in _one_ previous month.
