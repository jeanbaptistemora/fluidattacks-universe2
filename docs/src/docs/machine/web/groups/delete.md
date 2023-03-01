---
id: delete
title: Delete
sidebar_label: Delete
slug: /machine/web/groups/delete
---

When you determine
that a particular group
isn't necessary anymore,
you can proceed to delete it.
In order to do this,
first you need to go
to the **Scope** section
of the group you want to manage.

When you get to the **Scope** section,
scroll all the way down
until you see the part called
**Delete this group**
that has a button with the same name.
Be aware that this section
will only appear
if you have the appropiate authorization.

![Delete Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1668526136/docs/web/groups/delete/delete.png)

After clicking on this button
a window will appear
in which you will need to type the name
of the group you are currently managing.
Before this,
make sure that you want to proceed
with the deletion of the group,
as there is no going back
after you complete it.
With this consideration in mind,
after typing the name of the group,
click on **Confirm** button
to complete the deletion of the group.

![Delete Modal](https://res.cloudinary.com/fluid-attacks/image/upload/v1668526339/docs/web/groups/delete/action_delete.png)

## Reason why you want to delete the group

When you want to delete a group,
you will find eight reasons to do this action.
Below you can see the definitions of these reasons.

- **System will be deprecated:** It will not be further
  developed in those repositories that make up the group.

- **No more security testing:** No further testing of
  the group will be required, as the group is now closed.

- **Different security testing strategy:** Change of testing
  service provider.

- **Group rename:** The name of the group should be changed
  to a more appropriate name for the project.

- **Information will be moved to a different group:**
  The scope in that group will be moved to another
  group either because it will be merged with another
  project or because the information in it needs to be restructured.

- **PoC Over:** End of PoC time.

- **Testing Request Cancelled:** Before starting tests on a group,
  the customer cancels the order.

- **Other reasons not mentioned here:**
  Of the eight reasons given above,
  none apply to why the group is being closed.

> **Note:** This action will immediately delete the group.
> This will remove all of its data including
> findings and related vulnerabilities.
> This is a destructive action and cannot be undone.
