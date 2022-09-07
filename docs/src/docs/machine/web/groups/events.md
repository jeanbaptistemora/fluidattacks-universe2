---
id: events
title: Events
sidebar_label: Events
slug: /machine/web/groups/events
---

Sometimes,
a situation may arise in a
group that prevents our analysts
from pentesting part of the
scope or maybe all of it.
Your team needs to keep track
of these situations and solve them,
so we can resume our assessments.
The place on the ARM where you
can see a cumulative record of
solved and unsolved events in
your group is the Events section.

![Event Tab View](https://res.cloudinary.com/fluid-attacks/image/upload/v1661272950/docs/web/groups/events/event_tab.png)

This section shows a table
providing the following
information:

- **ID:**
  The event’s unique identifier
- **Root:**
  Refers to the
  nickname of the root.
- **Date reported:**
  When the event was reported
- **Description:**
  The problem that,
  according to the
  hacker,
  impeded,
  or still impedes,
  their security assessments
- **Type:**
  The category in which
  the problem falls,
  which can be Authorization
  for special attack,
  Incorrect or missing supplies,
  ToE different from what
  was agreed upon or Other
- **Status:**
  The condition of the event,
  which can be Solved,
  Pending, or Unsolved.
- **Date closed:**
  When the event was solved,
  if it was;
  otherwise,
  only a hyphen is shown

## Status in the event

The statuses help us to have more
clarity about the status of our events.
We handle three types:
Unsolved,
Pending,
and Solved.
Here we will explain
the flow of these.

First,
when an event is opened,
it will have the status **Unsolved**.

![Unsolved Status](https://res.cloudinary.com/fluid-attacks/image/upload/v1661276495/docs/web/groups/events/status_unsolved.png)

Here you have to give the
solution to this created event.
When you have it,
go to the checkbox on the
left and click on it.
When you do this,
the **Request Verification** option
will be activated immediately.

![Request Verification Option](https://res.cloudinary.com/fluid-attacks/image/upload/v1661276495/docs/web/groups/events/status_request_verification.png)

When you click on it,
you will get a pop-up window
where you will have to explain
the justification of how
you solved this event;
remember to enter at least ten characters,
followed by clicking on the **Confirm button**.

![Confirm Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1661276494/docs/web/groups/events/status_confirmb.png)

At this moment,
our event will enter
the **Pending state**,
where we will be waiting
for the verification that
the supplied solution is effective.

![Pending State](https://res.cloudinary.com/fluid-attacks/image/upload/v1661276495/docs/web/groups/events/state_pending.png)

When validated and the
solution successful,
it will move to our third **Solved state**.

![Solved State](https://res.cloudinary.com/fluid-attacks/image/upload/v1661276495/docs/web/groups/events/state_solved.png)

If this solution does not work,
the event will be set to
**Unsolved status**,
and you will receive a
notification where you will see
a comment from the analyst.
These comments will be sent
to you as a
[notification](/machine/web/notifications#consulting),
but you can also see them in the
[Comments](/machine/web/groups/events#event-details) tab.

## Functionalities

### Export events

You can download the event table
to a CSV (comma-separated values)
file by clicking on the Export button.

### Columns filter

You can show or hide columns
in the table by clicking on
the Columns button and toggling
the on/off button in front
of each column name.

![Columns Filter](https://res.cloudinary.com/fluid-attacks/image/upload/v1661272950/docs/web/groups/events/funct_filter_columns.png)

### Filters

By clicking the Filters button,
you can access several filter
options corresponding to the
variables that give columns
their names.

![Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1661272950/docs/web/groups/events/funct_filters.png)

## Event details

When you select an event,
you access a new section
with its details.
In the header,
you find the type
of event,
its ID,
the date it was reported
and its current status.

![Event Details Header](https://res.cloudinary.com/fluid-attacks/image/upload/v1652304172/docs/web/groups/events/details_events.png)

You can see three tabs
under the header: Description,
Evidence and Comments.
In **Description**,
you find why the event
was reported by one of
our hackers along
with their email,
the site where it is
present and the number
of components affected.

![Event Details Description](https://res.cloudinary.com/fluid-attacks/image/upload/v1652304172/docs/web/groups/events/details_description_authorization.png)

In **Evidence**,
you find images,
videos or GIFs justifying
the reported event.

![Event Details Evidence](https://res.cloudinary.com/fluid-attacks/image/upload/v1652304172/docs/web/groups/events/details_evidence.png)

In **Comments**,
you find the discussion
established between your
company's staff and
`Fluid Attacks'` hackers or
project managers about the event.
You can leave your comments there.

![Event Details Comments](https://res.cloudinary.com/fluid-attacks/image/upload/v1652304172/docs/web/groups/events/details_comments.png)

## Types of events

### Network access issues

The network port no
longer has internet access.

### VPN issues

Fails on the VPN connection.

### Remote access issues

Problems with connection methods.
For example,
when access to environmental
is not possible.

### Authorization special attack

A specific test needs to be performed,
which may affect availability
or integrity and requires
permission by the customer
to carry out a specific test.

### Client cancels project milestone

Customer cancels projects.

### Client explicitly suspends project

The client suspends the
project for a specified
time or excludes a
particular part of the ToE.

### Cloning issues

Some repository does not clone.

### Credential issues

No credentials exist,
or those that do exist
are not valid.

### Data update required

Reset user credentials or
data changes to consume a service.

### Environment issues

Problems in the environment,
either because it does not
open or because some flow
inside it has functional problems.

### Installer issues

Unable to install or error
when installed on mobile
or desktop application.

### Missing supplies

Lack of supplies
other than credentials.

### TOE differs approved

In One-Shot or continuous
service there are services
different from those agreed
upon or non-existent functionalities.

### Other

Any other problems that do not
fall into the above categories.

## Creating an event

In order to create a new event,
you need to click on the **New**
button in the **Event** tab.

![New Event Modal](https://res.cloudinary.com/fluid-attacks/image/upload/v1652281293/docs/web/groups/events/newevent_modal.png)

You will see the following pop-up window:

![Pop Up Window](https://res.cloudinary.com/fluid-attacks/image/upload/v1652281293/docs/web/groups/events/newevent_pop_up_window.png)

There you must enter or
select the requested information:

- The nickname of the
  root where the analyst
  discovered the event
  being reported
- The approximate date
  at which the event
  was discovered
- The type of event
- The affected accessibility
- A detailed description
  of the event
- Image or another file
  as supporting evidence
  of the event
- Impact on an ongoing
  reattack (Y/N).
  In case there is an impact,
  you must select the affected
  locations in the reattack
  so that it goes into the
  On-hold status.)

After entering the
information and clicking
the **Proceed** button,
the ARM will create the new
event and send an email to
all project managers.
You can also click on
the **Cancel** button
to discard the creation
of the event.

## Closing an event

When a user notifies that
the event has been solved,
or analysts find out they
can now access previously
blocked targets
without problems,
the event must be closed.

![Event Solved Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1652281293/docs/web/groups/events/markassolved_button_highlight.png)

You can do this in the
**Events** section.
You have to click on
the solved event.
Then,
in its description,
you will see the
**Mark as solved**
button that will show
you this pop-up window
when you click on it:

![Event Solved Window](https://res.cloudinary.com/fluid-attacks/image/upload/v1652281292/docs/web/groups/events/markassolved_window.png)

There you must enter the
date the analyst discovered
or was notified of the
solution of the event.
In addition,
you must provide the number
of hours that the event
affected the group.
Once this is done,
you can click the **Proceed**
button to mark the event as
solved or click the **Cancel**
button to interrupt this procedure.

## Update affected reattacks

With the
**Update affected reattacks**
button,
you can indicate that an
already created event
affects the execution of
one or more reattacks.

![Affected Reattacks Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1652281293/docs/web/groups/events/updateaffectedreattacks_button.png)

When you click on it,
you will see a pop-up
window where you can
select the respective
event and the reattacks
that are being affected.

![Affected Reattacks Window](https://res.cloudinary.com/fluid-attacks/image/upload/v1652281293/docs/web/groups/events/updateaffectedreattacks_window.png)

By clicking on the
**Proceed** button,
the selected reattack(s) will
go into a status called On hold.
(If you want to know
more about this status,
follow this [link](/squad/reattacks#reattacks-on-hold).)
By clicking on the
**Cancel** button,
you will abort the process.
