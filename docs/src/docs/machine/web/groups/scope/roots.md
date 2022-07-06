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

## IP roots

An IP address is the unique
identifier of a device on the
Internet or a local network.
When you provide us with an IP address,
we assess the security of all
web applications accessible
through this target.

To add a new IP root,
you need to go to the Scope
section of the group of your
choice and click on Add new root.
A pop-up window will appear,
asking you to enter the details
of the root (in this case,
IP address) you want to add.

![IP Roots](https://res.cloudinary.com/fluid-attacks/image/upload/v1657141769/docs/web/groups/scope/iproot_add_new.png)

Here are the definitions of
the details you need to enter:

- **Address:**
  IP address where the
  environment to be
  assessed is deployed.
- **Port:**
  Service endpoint of the
  environment within the device
  identified with the IP address.
- **Nickname:**
  An alternative name to
  easily identify the IP
  root in the future.

Once the IP address is added,
it will be listed below IP Roots.
There,
it is shown whether it is active.
Further,
you can export the information in
the table to a CSV (comma-separated values)
file by clicking on the **Export** button.

![IP Roots Export](https://res.cloudinary.com/fluid-attacks/image/upload/v1657141769/docs/web/groups/scope/iproot_export.png)

## URL roots

URL roots are dynamic
environments that have already
been deployed to a web server.
To add a new URL root,
go to the Scope section of the
group of your choice and click
on the Add new root button.
The following pop-up window will appear.

![URL Roots](https://res.cloudinary.com/fluid-attacks/image/upload/v1657141768/docs/web/groups/scope/urlroot_add_new.png)

The details you need to enter
are defined as follows:

- **URL:**
  Address where the
  environment is deployed.
- **Nickname:**
  An alternative name to
  easily identify the URL
  root in the future.

The URL roots you add will be
listed below **URL Roots**.
There,
it is shown whether it is active.
Further,
you can export the information in the
table to a CSV (comma-separated values)
file by clicking on the **Export** button.

![URL Roots Export](https://res.cloudinary.com/fluid-attacks/image/upload/v1657141769/docs/web/groups/scope/urlroot_export.png)

## Single root assessment

We assess only one
repository branch,
looking for vulnerabilities in
one single version of the system.
Testing only one branch allows
us to do a coherent assessment
and makes it easier to keep a
track of findings and fixes.
Therefore,
your development team can
efficiently manage the
reported vulnerabilities,
and our team can efficiently
verify the effectiveness of
the fixes you implemented.

## Adding a root with the SSH key

We know it is very important to keep our repositories
private if we have sensitive information in there.
A component that can help you achieve this purpose is
the SSH key (Security Shell), which you can use for authentication.
By setting SSH keys, you can connect to your repository
server without using a username and password.
If you need to set up an SSH Key,
we recommend reading this document:
[Use SSH keys to communicate with GitLab](https://docs.gitlab.com/ee/ssh/index.html#add-an-ssh-key-to-your-gitlab-account).
There, we show you how to generate your private
and public key step by step.

With a SSH key,
someone can clone your repository
and use that code according to their interests.
It is essential that you provide our hackers with
the most complete information and access rights
before they start hacking your software.
Here,
you will learn how to use the **Scope** tab for
adding SSH keys with **Adding a new root**.

On the ASM,
you can give full permission for
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

## Editing Git roots

If you want to edit the
details of an active root,
you need to click on it.
A pop-up window will appear,
where you can navigate
three tabs: **Git repository**,
**Environment URLs**
and **Secrets**.

![Edir Git Roots](https://res.cloudinary.com/fluid-attacks/image/upload/v1654884640/docs/web/groups/scope/root_editing_git_roots.png)

The Git repository tab allows
you to change details of your
Git repository.
Keep in mind that modifying the
repository’s URL and branch is
only allowed if absolutely no
vulnerabilities have been
reported in it.
If there are reported vulnerabilities,
you will have to add a new root
with the URL and branch you need
to include in the security tests.

## Deactivating roots

:::caution
Scope changes may involve closing or reporting new vulnerabilities
:::

Deleting a root isn't possible
in the ASM because in the
security world it is
always better to keep
records of everything.
However,
you can change its state
to **Active** or **Inactive**,
which would mean the following:

- **Active:**
  The repository is available and ready for our analysts to access.
- **Inactive:**
  The repository does not exist anymore, it was changed, or it was added by
  mistake.

We will notify the state changes
via email to all the people involved in the
project (both `Fluid Attacks’s`
and the customer’s users).

You can change the state at any moment.
We will keep track of every change for
traceability reasons.

### Out of scope

This option takes
the root out of scope,
therefore it will no
longer be tested.

### Registered by mistake

This option is useful in case
of mistakes when adding a root,
but if you just
need to update the URL,
branch or any other root attributes,
refer to [Editing git roots](#editing-git-roots)

### Moved to another group

This option allows moving a
root to another group along with the
vulnerabilities reported to it.

![Move root](https://res.cloudinary.com/fluid-attacks/image/upload/v1634230160/docs/web/groups/scope/move_root.png)

The search bar will suggest
other groups with the same
service type that you have
access to within the organization.

Then,
after clicking the "proceed" button,
the root will be deactivated in the
current group and created in
the selected group.

## Secrets

This section allows
you to see,
add,
edit and delete secrets.
These are usernames,
passwords,
email addresses,
tokens,
etc.,
that give us access to
private repositories
and environments.
As this is sensitive information
that has to be protected,
only a limited group of
people has access to it.
The management of secrets
is done for previously
created roots or URLs,
listed in the tables **Git Roots**
or **Environment URLs** in the
Scope section.

![Go to Secrets Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1652717752/docs/web/groups/scope/secrets_gitroots_table.png)

You can select a
root from Git Roots.
You will immediately see a
pop-up window with three tabs,
the third one being **Secrets**.

![Secrets Window](https://res.cloudinary.com/fluid-attacks/image/upload/v1652717752/docs/web/groups/scope/secrets_window.png)

To add a new secret,
you have to access the Secrets
section and click on the
**Add secret** button.

![Add Secret Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1652717752/docs/web/groups/scope/secrets_click_add.png)

The secret must consist
of key and value.
Additionally,
you can include a short description.

![Add Secrets](https://res.cloudinary.com/fluid-attacks/image/upload/v1652717752/docs/web/groups/scope/secrets_add_window.png)

When you click Proceed,
the secret is made accessible
to our hackers on the ASM.
You can also delete or edit
all the secrets you add by
clicking on the
corresponding button.

![Secret Details](https://res.cloudinary.com/fluid-attacks/image/upload/v1652717752/docs/web/groups/scope/secrets_accesible_editing.png)

From Environment URLs,
you have to select the URL
where you want to add,
delete or edit secrets and
follow the same procedure
described above.

## Existing credentials

Credentials help us to have
access to one or multiple
repositories.
When creating or
editing a root,
you can see the
**Existing credentials** field.
Clicking on it will display a
list of credentials previously
used for other repositories.

![Existing Credentials Field](https://res.cloudinary.com/fluid-attacks/image/upload/v1654800380/docs/web/groups/scope/roots_existcredentials_field.png)

If any of the credentials in
the list is useful for the root
that you want to create or edit,
select it,
and the **Credential type** and
**Credential name** fields will
be autofilled.

![Credentials Type](https://res.cloudinary.com/fluid-attacks/image/upload/v1654800380/docs/web/groups/scope/roots_existcredentials_field2.png)
