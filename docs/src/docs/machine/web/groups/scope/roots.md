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

## Adding a root with the SSH key

We know it is very important to keep our repositories
private if we have sensitive information in there.
A component that can help you achieve this purpose is
the SSH key (Security Shell), which you can use for authentication.
By setting SSH keys, you can connect to your repository
server without using a username and password.
If you need to set up an SSH Key, we recommend reading
this document: [Use SSH keys to communicate with GitLab](https://docs.gitlab.com/ee/ssh/index.html#add-an-ssh-key-to-your-gitlab-account).
There, we show you how to generate your private
and public key step by step.

With a SSH key, someone can clone your repository
and use that code according to their interests.
It is essential that you provide our hackers with
the most complete information and access rights
before they start hacking your software.
Here, you will learn how to use the **Scope** tab for
adding SSH keys with **Adding a new root**.

On the ASM, you can give full permission for
accessing your Git repository in the “Scope” tab
using the **Add new root** option.
The nice feature we have here is a Cloning
credential with the Repository SSH Key.
We want to guide you on how to do it.
So let’s start!

- First, log in to the ASM and go to the Scope tab.
  There, you can find the Add new root button.

![Scope Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1643749134/docs/web/groups/scope/root_scope_tab.png)

- When you click on **Add new root**, a pop-up window
  will show up where you need to fill out the
  information with your Git repository.

![Add New Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1643749134/docs/web/groups/scope/root_add_new.png)

- Fill out the **Cloning credential** field with
  your SSH Private Key.
  You need to select **SSH** from the drop-down
  menu in the **Type** field.
  After that, an extra field will appear,
  asking for your private key.

![Clone Credential](https://res.cloudinary.com/fluid-attacks/image/upload/v1643749134/docs/web/groups/scope/root_cloning_credential.png)

- After filling out all the fields, click on **Proceed**.
  You will have your new URL in Git Roots

## Editing root by SSH key

If you already have your Git roots but
want to add the SSH keys or edit them,
this is very easy to do.

- First, log in to our ASM and click
  on the **Scope** tab.
  There, you can see all the Git roots URLs.

![Edit Scope Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1643814404/docs/web/groups/scope/edit_scope_tab.png)

- You need to pick which URL you want to edit.
  When you click on it, the **Edit root** window
  will pop up, where you can edit your root.

![Edit Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1643814403/docs/web/groups/scope/edit_window_root.png)

- Provide your SSH private key in
  the **Cloning credentials** field.
  Then, choose SSH from the **Type**
  drop-down menu.
  After that, an extra field will
  appear, asking for your private key.

![Clone Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1643814403/docs/web/groups/scope/edit_cloning_credentials.png)

- After filling out all the fields,
  click on **Proceed** and your changes
  will be automatically applied.

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

## Deactivating roots

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
