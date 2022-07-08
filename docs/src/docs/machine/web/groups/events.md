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
The place on the ASM where you
can see a cumulative record of
solved and unsolved events in
your group is the Events section.

![Event Tab View](https://res.cloudinary.com/fluid-attacks/image/upload/v1652798987/docs/web/groups/events/event_tab_view.png)

This section shows a table
providing the following
information:

- **ID:**
  The event’s unique identifier
- **Date reported:**
  When the event was reported
- **Description:**
  The problem that,
  according to the
  hacker,
  impeded,
  or still impedes,
  their security assessments
- **Accessibility:**
  Which out of Environment,
  Repository or both are
  affected by the event
- **Affected components:**
  The components that are
  showing problems within
  the repository or environment
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
  which can be either Solved
  or Unsolved
- **Date closed:**
  When the event was solved,
  if it was;
  otherwise,
  only a hyphen is shown

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

![Columns Filter](https://res.cloudinary.com/fluid-attacks/image/upload/v1652799131/docs/web/groups/events/functionalities_columns_filter.png)

### Filters

By clicking the Filters button,
you can access several filter
options corresponding to the
variables that give columns
their names.

![Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1652799132/docs/web/groups/events/functionalities_filters.png)

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

### Authorization for special attack

This event type corresponds to
situations when the hacker
requests permission to
exploit a vulnerability,
anticipating that its
exploitation may cause
anomalous behaviors in your
system’s infrastructure or environment.

### Incorrect or missing supplies

This event type refers to
situations when the testing
environment is down or when
you provide incorrect URLs
or bad credentials.

### ToE different from what was agreed upon

This event type refers to
situations when you add a
git repository or environment
that we didn’t agree to assess
when the ToE was defined.

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
the ASM will create the new
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
