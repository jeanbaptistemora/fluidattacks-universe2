---
id: roots
title: Roots
sidebar_label: Roots
slug: /machine/web/groups/scope/roots
---

In this section of the Scope tab,
you can add and edit
the repositories and environments
to be included in the testing service

## Adding git roots

![Git Root Buttons](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211880/docs/web/groups/scope/git_root_buttons_pviqnf.webp)

By clicking on the "Add new root" button, the following form will show up:

![Add New Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211896/docs/web/groups/scope/add_new_root_nql2hc.webp)

Here you can specify the URL of the repository, the specific branch, and the
kind of environment to which it corresponds

You can also choose
if you would like a Health Check
for the existing code,
which means that we would also review
all the code already in the repository
at the moment the project starts,
for an additional cost.

Lastly, you can specify the paths to
[exclude](/machine/web/groups/scope/exclusions)
from the testing scope.

After you complete the required fields,
click on **Proceed**
to add the git Root,
or you can click on **Cancel**
to discard all the information.

## Editing git roots

To edit a git root, click the desired row on the table and the following form
will show up:

![Edit Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211880/docs/web/groups/scope/edit_root_whbob4.webp)

You can update the branch, environment kind,
activate or deactivate the Health Check option,
modify the [exclusions](/machine/web/groups/scope/exclusions), and if there
are no active vulnerabilities reported, you can also update the URL.

Then, click on **Proceed**
to apply the changes
or on **Cancel** to discard them.

### Managing git root environments

In the edit modal, authorized users will also find the **Environment URLs**
tab:

![Manage environments](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211895/docs/web/groups/scope/manage_envs_ywyggq.webp)

You can click on the **plus(+)** button
to add the environment URLs
corresponding to the selected git Root,
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

Deleting a root isn't possible in the ASM because in the security world it is
always better to keep records of everything.
However, you can change its state to **Active** or **Inactive**, which would
mean the following:

- **Active:**
  The repository is available and ready for our analysts to access.
- **Inactive:**
  The repository does not exist anymore, it was changed, or it was added by
  mistake.

We will notify the state changes via email to all the people involved in the
project (both Fluid Attacks’s and the customer’s users).

You can change the state at any moment. We will keep track of every change for
traceability reasons.

### Out of scope

This option takes the root out of scope, therefore it will no longer be tested.

### Registered by mistake

This option is useful in case of mistakes when adding a root, but if you just
need to update the URL, branch or any other root attributes,
refer to [Editing git roots](#editing-git-roots)

### Moved to another group

This option allows moving a root to another group along with the
vulnerabilities reported to it.

![Move root](https://res.cloudinary.com/fluid-attacks/image/upload/v1634230160/docs/web/groups/scope/move_root.png)

The search bar will suggest other groups with the same service type that you
have access to within the organization.

Then, after clicking the "proceed" button, the root will be deactivated in the
current group and created in the selected group.
