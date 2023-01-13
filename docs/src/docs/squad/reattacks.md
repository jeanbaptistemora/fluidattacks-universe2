---
id: reattacks
title: Reattack
sidebar_label: Reattack
slug: /squad/reattacks
---
When you have applied a solution for an existing vulnerability,
you can request a reattack
for us to validate its effectiveness.
You can do this from the
[Locations](/machine/web/vulnerabilities/management/vulnerability-assignment)
and
[To-DoList](/machine/web/vulnerabilities/management/to-do-list)
sections of the ARM.
The steps required are
fundamentally
the same in both sections.
Here,
we show you how to do
it from Locations.

1. Log into your ARM account
  and click on one of your
  groups to access it.
  Once inside the group,
  you will see a list of all
  the types of vulnerabilities it has.

   ![Group Vulnerabilities Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1665174418/docs/squad/reattack/vuln_view.png)

1. Now look for the type of vulnerability
  that contains the individual vulnerability
  or vulnerabilities
  for which you want to request a reattack
  are grouped and click on it.
  By doing this,
  you will land on the **Locations** tab
  of the type of vulnerability you chose.
  You can select only open vulnerabilities,
  and only those whose reattack status
  is neither Requested nor On_hold
  are eligible for reattacks.
  When you have made your selection,
  click on the **Reattack** button
  on the right-hand side of the screen.

   ![Enabled Reattacks Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1665174541/docs/squad/reattack/reattack_action.png)

1. The following form will appear
  where you will have to explain
  the applied solution.

   ![Reattack Request Form](https://res.cloudinary.com/fluid-attacks/image/upload/v1665174597/docs/squad/reattack/justification_reattack.png)

1. After requesting the reattack,
  you will see the word **Requested**
  in the **Reattack** column corresponding
  to that vulnerability.
  From then on,
  you will have to wait for the
  response from the `Fluid Attacks` team.
  The latter’s response time will
  comply with the conditions set forth
  in the service-level agreements.

   ![Reattack Requested](https://res.cloudinary.com/fluid-attacks/image/upload/v1665174651/docs/squad/reattack/requested_state.png)

1. In the **Consulting** tab,
  you will see a new comment related
  to the justification you gave when
  requesting the reattack.
  In this same tab,
  our hackers can generate other
  comments and notify the decision
  taken on your request.

   ![Consulting Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1665174707/docs/squad/reattack/consul_reattack.png)

## Reattack outcomes

The reattack status will be
**Verified (open)** if the
vulnerability you requested
to reattack is still exploitable.
Our hackers will give you
evidence of how it was exploited,
which you can access in the
**Evidence** tab.

![Evidence Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1665174749/docs/squad/reattack/evidence_reattack.png)

If the vulnerability is still open
and you cannot close it for the moment,
you can consider defining other
[treatments](/machine/web/vulnerabilities/management/treatments).
One of them is
**Permanently accepted vulnerability**.
However,
you can later try to remediate
this vulnerability and
[request a reattack](/machine/web/vulnerabilities/management/treatments/#reattacking-a-permanently-accepted-vulnerability)
to verify its remediation.

The status will be **Verified (closed)**
if the vulnerability you requested
to reattack has been proven by our
hackers to have been successfully
remediated.

## Reattacks on hold

Sometimes reattacks are delayed
due to [events](/machine/web/groups/events)
in your environment,
and having to send another
reattack request can be tedious.
That is why the ARM has the
**On_hold** status for reattacks.
This status denotes when
reattack requests are put on hold.
When the events are solved,
the reattack request is
automatically reactivated
without having to be repeated.
This use of automation provides
agility to the reattack process.

![Verified Closed](https://res.cloudinary.com/fluid-attacks/image/upload/v1647974013/docs/squad/reattack/reattack_on_hold.png)

:::tip free trial
**Search for vulnerabilities in your application for free!**
Start your [21-day free trial](https://fluidattacks.com/free-trial/)
and discover the benefits of our [Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/)
[Machine Plan](https://fluidattacks.com/plans/).
:::
