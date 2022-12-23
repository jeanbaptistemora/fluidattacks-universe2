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

If your group has
[White services](/about/glossary/#white-box)
it will have [Git Roots](/machine/web/groups/scope/roots/#git-roots)
and [Environment URLs](/machine/web/groups/scope/roots/#environment-urls-table),
or if your group has [Black services](/about/glossary/#black-box),
you will have [IP Roots](/machine/web/groups/scope/roots/#ip-roots)
and [URL roots](/machine/web/groups/scope/roots/#url-roots).

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

## Git Roots table

The Git Roots table gives us
summary information of the
repositories I want to be analyzed.

![Git Root table](https://res.cloudinary.com/fluid-attacks/image/upload/v1668103427/docs/web/groups/scope/git_root_table.png)

This table shows the following information:

- **URL:**
  Refers to the URL of the
  repository where the code
  to be cloned is located.
- **Branch:**
  The branch I am going to clone.
  Remember we assess only one
  repository branch per group.
  For more information click
  [here](/machine/web/groups/scope/roots/#single-root-assessment)
- **State:**
  There are two states:
  **Active and Inactive**.
  **Active** means that the root
  is being tested and
  **Inactive** means that the root
  is no longer being tested.
- **Status:**
  There are five:
  Cloning,
  OK,
  Failed,
  N/A and Unknown.
  For more information click
  [here](/machine/web/groups/scope/roots/#status-in-git-root)
- **HCK:**
  If Health Check is included
  in that repository.
- **Nickname:**
  The nickname of this repository
  to be easily identified.
- **Sync:**
  Request to clone that repository
  once again since changes have been
  generated and it is required to
  have it updated.

There is also a **downward-facing arrow**
on the left of the Type column,
which,
upon click,
will unfold the description for
each repository.

![Downward-facing arrow](https://res.cloudinary.com/fluid-attacks/image/upload/v1668103621/docs/web/groups/scope/downward.png)

## Git Roots functionalities

### Add new root

To add a new Root,
you must click on the
box **add new root**.
There you will get a pop-up
window where you will have to
enter the information of the
new repository you want to add.

![Add New Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1668103688/docs/web/groups/scope/add_new_gitroot.png)

The information you have to fill in is as follows:

- **URL:**
  The URL where the
  repository is located.
- **Branch:**
  The branch that is inside
  the repository that I want
  to be validated.
- **Nickname:**
  The nickname of the root
  to remember it easily.
- **Existing credentials:**
  Existing credentials can be reused.
  For more information,
  click
  [here](/machine/web/groups/scope/roots#existing-credentials).
- **Credential Type:**
  To have access to the repository,
  we have to have access to
  the credentials,
  which are three types:
  HTTPS,
  Azure DevOps PTA and
  SSH.
  Here,
  you select which type of
  credential you want to add.
  For more information,
  click [here](/machine/web/groups/scope/roots/#protocols-to-clone-a-git-repository)
- **Environment kind:**
  The type of environment that is this root.
- **Health Check:**
  You have to put YES or NO
  if this git root applies
  Health Check.
- **Exclusions:**
  Specifies what files of that
  root will be ignored during
  the analysis by clicking on
  the plus symbol;
  you can add many as you need.
  If you want to know how to do it,
  you can enter [here](/machine/web/groups/scope/exclusions).

When you fill in the required fields,
click on **Confirm**,
and your repository will
be successfully added.

### Export button

Clicking on the **Export**
button will download a file
with CSV (comma-separated
values) extension,
which contains the information
in the Git Root table.

### Columns filter

Columns filter helps us to
show or hide which columns I
want to see in the Git Roots table.
By clicking on the toggling
on/off button in front
of each column name,
you can manipulate the
information to display
in the table.

![Columns Filter](https://res.cloudinary.com/fluid-attacks/image/upload/v1668104380/docs/web/groups/scope/columns_filter.png)

### Filters

We have five different filters
in the Git Roots section,
helping us filter the information
that is of interest quickly and safely.

![Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1668104488/docs/web/groups/scope/general_filters.png)

### Managing Git Root

If you want to edit the details
of an active root,
you need to click on it.
A pop-up window will appear,
where you can navigate three tabs:
[Git repository](/machine/web/groups/scope/roots/#git-roots),
[Environment URLs](/machine/web/groups/scope/roots/#environment-urls-table)
and [Secrets](/machine/web/groups/scope/roots/#secrets)

![Managing Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1668171709/docs/web/groups/scope/managing_git_root.png)

The Git repository tab allows you
to change details of your Git root.
Keep in mind that modifying the
repository’s URL and branch is only
allowed if absolutely no vulnerabilities
have been reported in it.
If there are reported vulnerabilities,
you will have to add a new root
with the URL and branch you need
to include in the security tests.

If you want to know how to edit
or add an environment,
enter [here](/machine/web/groups/scope/roots/#managing-git-root-environments).
Now,
if you're going to add or edit secrets,
you can learn how to do it
[here](/machine/web/groups/scope/roots/#secrets).

### Deactivate a Git Root

:::caution
Scope changes may involve closing or reporting new vulnerabilities
:::

Deleting a root isn't possible
in the ARM because in the
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

To do this action of change of state,
you must first find the branch
you want to disable or move to.
Once you know which one it is,
go to the state column and
click on the toggle of the
branch that is currently active.

![Deactivate Git Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1668182871/docs/web/groups/scope/toggle_brach.png)

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

#### Registered by mistake

This option is useful in case
of mistakes when adding a root,
but if you just
need to update the URL,
branch or any other root attributes,
refer to [Managing Git Root](/machine/web/groups/scope/roots/#managing-git-root).

#### Moved to another group

This option allows moving a
root to another group along with the
vulnerabilities reported to it.

![Move root](https://res.cloudinary.com/fluid-attacks/image/upload/v1668183656/docs/web/groups/scope/move_other_group.png)

The search bar will suggest
other groups with the same
service type that you have
access to within the organization.

#### Other

When neither of the previous two
reasons applies,
then you can use this one and
put what the reason is.

Then,
after clicking the **"Cofirm"** button,
the root will be deactivated in the
current group and created in
the selected group.

## Credential Type

To clone a Git repository in
the Scope section,
you can do it with:
**Protocol HTTPS (User and Password),**
**SSH key (Security Shell)**
or **Azure Organization (Access Token)**.
You can use any of these for authentication.

### Adding a root with the HTTPS​ (User and Password)​

With HTTPS you can access by
putting **User** and **Password**.

![Adding Root HTTPS](https://res.cloudinary.com/fluid-attacks/image/upload/v1670942450/docs/web/groups/scope/https.png)

When selecting **User** and
**Password option**,
you have to fill in the fields that
say **Repository user** and
**Repository password**,
followed by clicking on the
**Check Access button**.

![Adding Root Option](https://res.cloudinary.com/fluid-attacks/image/upload/v1670942553/docs/web/groups/scope/password_user.png)

Remember that the **Check Access**
button helps us to validate if the
access credentials given are
correct to perform the
cloning successfully.
If they are not,
you will get invalid Credentials,
and if they are valid,
you will get Success access.

### Adding a root with the SSH key

With SSH keys,
you can connect to your repository
server without using a username and password.
Here you have to supply a Private Key.
If you need to set up an SSH Key,
we recommend reading this document:
[Use SSH keys to communicate with GitLab](https://docs.gitlab.com/ee/ssh/index.html#add-an-ssh-key-to-your-gitlab-account)
.
To add such a credential,
click on the **SSH** option.
Here will enable the **Private SSH Key**
field for you to add.

![Adding Root SSH](https://res.cloudinary.com/fluid-attacks/image/upload/v1670942728/docs/web/groups/scope/ssh.png)

Remember to click on the
**Check Access** button
or validation if the credential
gives access to clone the repository.

### Adding a root with the Azure DevOps PTA

**Azure DevOps** is a platform that
provides software development services,
among those able to have repository
management and control the source code.
We invite you to access the official
documentation of
[Azure DevOps](https://learn.microsoft.com/en-us/azure/devops/user-guide/what-is-azure-devops?toc=%2Fazure%2Fdevops%2Fget-started%2Ftoc.json&view=azure-devops)
if you want more information.

In the ARM,
if you want to add
**Azure DevOps PTA (Personal Access Token)**
repositories, you have to select
that type of credential.
There,
you will be prompted for a Repository
access token and Azure Organization.

![Adding Root azure](https://res.cloudinary.com/fluid-attacks/image/upload/v1670943031/docs/web/groups/scope/azure.png)

After entering these data,
click on **Check Access**.
If the information given is correct,
the Root will be created successfully.

:::note
Remember that you can also add
all this credentials types in
**Global Credential**.
For more information,
click [here](/machine/web/machine/web/global-credentials/).
:::

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

## Environment URLs

Here you see the environments
according to the Git Roots
added to them.

## Environment URLs table

In the environments table,
you can see the environments
added in Git Roots.

![Environment URL Table](https://res.cloudinary.com/fluid-attacks/image/upload/v1659123650/docs/web/groups/scope/env_url_table.png)

There is also a downward-facing
arrow on the left,
which,
upon click,
it shows you the creation date
and the Git Root corresponding
to that registered environment.

![Environment Registered](https://res.cloudinary.com/fluid-attacks/image/upload/v1659123650/docs/web/groups/scope/env_url_registered.png)

## Managing git root environments

Authorized users will also find the
**Environment URLs** tab in the edit modal.
You can add environments corresponding
to the selected git Root by clicking
on the **Add Environment URL** button.

![Environment URLs Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1659121166/docs/web/groups/scope/managing_tab.png)

Here you will get a popup window
where you will have to select which
environment URL type you want to
add and the URL of this one,
followed by clicking Confirm.

![Add Environment](https://res.cloudinary.com/fluid-attacks/image/upload/v1659121166/docs/web/groups/scope/managing_environment_select.png)

You will get the added
environment successfully.
Remember that you can also delete
any environment by clicking on
the trash button.

![Environment Added](https://res.cloudinary.com/fluid-attacks/image/upload/v1659121166/docs/web/groups/scope/managing_added.png)

:::note
You can also find in the Environment URLs
view how to add secrets.
Click [here](/machine/web/groups/scope/roots#secrets)
if you want to know more.
:::

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
to our hackers on the ARM.
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
