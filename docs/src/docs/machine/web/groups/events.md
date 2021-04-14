---
id: events
title: Events
sidebar_label: Events
slug: /machine/web/groups/events
---

Sometimes, a situation may arise for a group that prevents analysts from pentesting part
of the scope or maybe all of it. When this is the case we need to keep track of these
situations and manage them, so we can resolve them quickly and efficiently. This is what
the **Event** tab is used for.

![Event Tab View](/img/web/groups/events/event_tab_view.png)

### Creating an event

In order to create a new event, you need to click on the **New** button that is in the
**Event** tab. Then, a pop-up will appear for creating the event.

![New Event Modal](/img/web/groups/events/newevent_modal.png)

Here you must enter all the information about the event including:

- The approximate date and time at which the event was discovered.
- Select the type that better summarizes the event.
- The location at which the analyst was when the event was discovered.
- Specify if the event affects accesibility to the **Environment**, **Repository** or both.
- A more detailed description about the event.
- The action you were performing before being blocked by the event and what you would do
after the block.
- Evidence of the event presented in an image or a file.

After the entering the information and pressing the **Proceed** button, the ASM will create
a new event and send an email to all project managers. You can also click on the **Cancel**
button to dismiss the creation of the event.

### Closing an event

When a group user notifies that the event has been solved or the analysts find out
that they can now access the previously blocked targets with no problems, then it is time
to close the event.

![Event Solved Button](/img/web/groups/events/markasolved_button_highlight.png)

This can be done by entering the **Event** tab and clicking on the event that wa solved,
then in the description of the event there will be a button called **Mark as solved**.
When you click it, a pop-up will appear.

![Event Solved Modal](/img/web/groups/events/markasolved_modal.png)

In here you must specify the date that the analyst was notified about or discovered that
the event had been solved, and also provide the number of hours that the event affected
the group. With this done you can click on **Proceed** to mark the event as solved, and
now it will appear closed in the event table.
