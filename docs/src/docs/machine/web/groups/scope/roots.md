---
id: roots
title: Roots
sidebar_label: Roots
slug: /machine/web/groups/scope/roots
---

In this section of the Scope tab,
you can add and edit the repositories
and environments to be included
in the testing service.
If you want to know more
about these service types,
click [here](/machine/web/groups/services).

## Git Roots

Here we put any Git repositories
composed of code to clone and
start the analysis of these.
In Git Roots,
you can add,
edit,
enable or disable the root.
You can also export and filter
the information of all your
Roots that compose the table.

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
repository branch per group,
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

## Protocols to clone a Git repository

To clone a Git repository
in the Scope section,
you can do it with the
protocol **HTTPS** or
**SSH key (Security Shell)**,
which you can use for authentication.

## Adding a root with the HTTPS​

With HTTPS,
you can access it in two ways:
**User and Password**
or **Access Token**.

![Adding Root HTTPS](https://res.cloudinary.com/fluid-attacks/image/upload/v1658955062/docs/web/groups/scope/adding_root_https.png)

When selecting
**User and Password** option,
you have to fill in the fields
that say **Repository user**
and **Repository password**,
followed by clicking on the
**Check Access** button.

![Adding Root Option](https://res.cloudinary.com/fluid-attacks/image/upload/v1658955062/docs/web/groups/scope/adding_root_option.png)

Remember that the **Check Access**
button helps us to validate if the
access credentials given are
correct to perform the
cloning successfully.
If they are not,
you will get invalid Credentials,
and if they are valid,
you will get Success access.

## Adding a root with the SSH key

With SSH keys,
you can connect to your repository
server without using a username and password.
Here you have to supply a Private Key.
If you need to set up an SSH Key,
we recommend reading this document:
[Use SSH keys to communicate with GitLab](https://docs.gitlab.com/ee/ssh/index.html#add-an-ssh-key-to-your-gitlab-account)
.
We show you how to generate
your private and public keys
step by step.

![Adding Root SSH](https://res.cloudinary.com/fluid-attacks/image/upload/v1658955062/docs/web/groups/scope/adding_root_ssh.png)

Remember to click on the
**Check Access** button
or validation if the credential
gives access to clone the repository.

### Managing git root environments

In the edit modal, authorized users will also find the **Environment URLs**
tab:

![Manage environments](https://res.cloudinary.com/fluid-attacks/image/upload/v1659021837/docs/web/groups/scope/manage_envs_ywyggq.png)

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

## Deactivate a Git Root

It may be that over time we
no longer require the use
of some repositories,
or we want to move it
to another group.
We have the flexibility to
inactivate or move repositories
quickly and easily by going
to the State column.

![Deactivate Git Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1659017040/docs/web/groups/scope/deactivate_git_root.png)

First, you must find the branch
you want to disable or move to.
Once you know which one it is,
go to the state column and click
on the toggle of the branch
that is currently active.
Here,
you will get pop-up window
asking why you want to
disable the root.

![Deactivate Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1659017040/docs/web/groups/scope/deactivate_root_windw.png)

When you click on the drop-down menu,
you will get three options:
Registered by mistake,
move to another group,
and other.
Remember that each action you
select must take into account
the alert warnings.
For more information,
click
[here](/machine/web/groups/scope/roots#deactivating-roots).

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

## Status in Git Root

The status help us to see how our
repository is in the cloning process.
We manage a total of 5 status.

- **Cloning:**
  The repository is being cloned.
- **Ok:**
  The cloning was successful.
- **Failed:**
  Something went wrong with the cloning.
- **N/A:**
  The root is inactive.
- **Unknown:**
  Is the initial state
  when creating a root,
  meaning it has not yet
  been cloned or is glued
  for this action.

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
