---
id: roots
title: Roots
sidebar_label: Roots
slug: /machine/web/groups/scope/roots
---

In this section of the Scope tab,
you can add and edit
the repositories and environments
that we should take into account
when performing penetration tests.
In order to do this,
you can click on one
of the three buttons
that allow you to do
different things.

## Add a git root

![Git Root Buttons](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211880/docs/web/groups/scope/git_root_buttons_pviqnf.webp)

By clicking on
the "Add git root" button
the following form
will show up

![Add New Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211896/docs/web/groups/scope/add_new_root_nql2hc.webp)

In here you can specify
the URL of your repository,
the specific branch
that we will use
to perform the penetration test
and the kind of environment
that it points to.

You can also choose
if you would like a Health Check
for the existing code,
which means that we would also review
all the code already in the repository
at the moment the project starts,
for an additional cost.

Lastly,
there are some fields
used to exclude
specific paths
from the group scope,
you can read
the details about this
in [this page](/machine/web/groups/scope/exclusions).

After you complete the required fields,
you can click on **Proceed**
to add the Git Root,
or you can click on **Cancel**
to discard all the information.

## Edit a git root

In order for the next button,
**Edit root**,
to become available
you must first click
on one of the git roots you already added
and the same form will show up again,
albeit slightly different

![Edit Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211880/docs/web/groups/scope/edit_root_whbob4.webp)

The form will have all the information
of the Git Root you selected
for you to modify.
You can change its environment kind,
activate or deactivate the Health Check option,
add more gitignores
or delete them by clicking on the trash icon
to the right of the specific gitignore
you would like to delete.

Again,
you can click on **Proceed**
to apply the changes
or on **Cancel** to discard them.

You might also wonder
how to delete a git root,
however this isn't possible in the ASM
because in the security world
it is always better
to keep records of everything.
What you can do is change a repository state
to **Active** or **Inactive**,
which would mean the following:

- **Active:**
  The repository is available
  and ready for our analysts
  to access.
- **Inactive:**
  The repository does not exist anymore,
  it was changed,
  or it was added by mistake.

Every time a repository is changed,
a notification will be sent
to all the people involved in the project
(both Fluid Attacks’s and the customer’s users).
Finally,
the states can be changed
by project users at any moment,
and every change will be stored
for future needs.

## Manage a git root environment

And lastly,
after selecting one of your added **Git Roots**,
you can also click on the **Manage environments** button
for the following form to show up

![Manage environments](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211895/docs/web/groups/scope/manage_envs_ywyggq.webp)

You can click on the **plus(+)** button
to add the environment URLs
corresponding to the selected Git Root,
and also delete them
by clicking on the trash button
to the right of the URL field.
To discard or apply the changes
you can click on **Cancel**
or **Proceed** respectively.

## Deactivating a root

:::caution
Scope changes may involve closing or reporting new vulnerabilities
:::

### Out of scope

This option takes the root out of scope, therefore it will no longer be tested.

### Registered by mistake

This option is useful in case of mistakes when adding a root, but if you just
need to update the url, branch or any other root attributes,
refer to [Edit a git root](#edit-a-git-root)

### Moved to another group

This option allows moving a root to another group along with the
vulnerabilities reported to it.

![Move root](https://res.cloudinary.com/fluid-attacks/image/upload/v1634230160/docs/web/groups/scope/move_root.png)

The search bar will suggest other groups with the same service type that you
have access to within the organization.

Then, after clicking the "proceed" button, the root will be deactivated in the
current group and created in the selected group.
