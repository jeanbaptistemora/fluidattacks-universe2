---
id: global-credentials
title: Global credentials
sidebar_label: Global credentials
slug: machine/web/global-credentials
---

In this section,
you will be able to perform two actions:
[Add credentials](/machine/web/machine/web/global-credentials/#organization-credentials)
at the organization level
and perform the connection via
[OAuth](/machine/web/machine/web/global-credentials/#add-repositories-via-oauth)
to the providers,
which are: **GitLab - GitHub - Bitbucket - Azure**.

## Organization credentials

You can store the credentials at
the organization level and use
them in all the groups that make
up the organization.
To see the credentials that exist,
you have to go to the main page
in the tab called credentials.

![Main Page](https://res.cloudinary.com/fluid-attacks/image/upload/v1670949034/docs/web/credentials/globla_credentials.png)

## Credentials table

Here you can see the list
of all the credentials created
in the organization you are located in.
In total, we have three columns which
are described below:

- **Name:**
  The name of the credential.
- **Type:**
  Which type of credential it is,
  can be [HTTPS](/machine/web/groups/scope/roots#adding-a-root-with-the-https-user-and-password),
  [SSH](/machine/web/groups/scope/roots#adding-a-root-with-the-ssh-key)
  or [Azure DevOps PAT](/machine/web/groups/scope/roots#adding-a-root-with-the-azure-devops-pat).
  You can also see in this column the connection
  of the providers via
  [OAuth](/machine/web/machine/web/global-credentials#add-repositories-via-oauth).
- **Owner:**
  The person who created the credential.

## Functionalities​

### Add

When you click on the Add button,
you will get a pop-up window
where you can add new credentials.

![Add Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1660670043/docs/web/credentials/credent_add_button.png)

Here,
you will have to enter a unique
credential name and select the
credential type (
[HTTPS](/machine/web/groups/scope/roots/#adding-a-root-with-the-https),
[SSH](/machine/web/groups/scope/roots/#adding-a-root-with-the-ssh-key)
or [Azure DevOps PAT](/machine/web/groups/scope/roots#adding-a-root-with-the-azure-devops-pat)).

### Edit

To edit an existing credential,
you have to select which
one you want to edit.
A pop-up window will appear,
where you have to click on
the toggle that says **New secrets**
to enable editing of the credential
and change its information.

![Edit Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1660670043/docs/web/credentials/credent_edit_button.png)

According to the Credential type
will enable the fields for editing.

### Remove

To delete a credential,
you have to select which
one you want to delete;
a warning window will appear
asking for your confirmation.

![Remove Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1660670043/docs/web/credentials/credent_remove.png)

The following are some points to
keep in mind regarding credentials:

- If the credential is removed,
  it is also removed from all
  the git roots used.
- When a stakeholder is removed
  from the organization,
  then their credentials are
  removed from that organization.
- The owner of the credentials
  is the last one that edited
  the credential's secrets.

### Search bar

The search bar filters the information
contained in the columns of the table.

## Add repositories via OAuth

You can connect directly to code service
providers such as
**GitLab - GitHub - Bitbucket - Azure**
from the
[ARM platform](/machine/web/arm/)
via **OAuth (Open Authorization)**,
which will allow us to connect the ARM to the provider,
where users authorize the flow of access
and thus will be able to access all the
repositories that you have in these.

![service providers](https://res.cloudinary.com/fluid-attacks/image/upload/v1676278513/docs/web/credentials/Four_providers.png)

> **Note:** These are the four providers that support the ARM.

We will now perform a step-by-step example using the GitLab provider.

The first step is to go to the **Global Credentials** view,
where you can select the provider of your
convenience that you want to authorize to connect to the ARM.

![Gitlab provider](https://res.cloudinary.com/fluid-attacks/image/upload/v1676278513/docs/web/credentials/Four_providers.png)

When you click on it,
you will be redirected to the **provider's authorization** page,
where you will be asked to authorize the
connection between the ARM and your account.
When you click on **Authorize**,
the connection between these two services will be established.

![Authorize provider](https://res.cloudinary.com/fluid-attacks/image/upload/v1676280659/docs/web/credentials/authorize.png)

When you authorize,
you will be redirected to the ARM
to the [Global Credentials](/machine/web/machine/web/global-credentials)
view,
where you can see the new credential created as OAuth.

![credential create](https://res.cloudinary.com/fluid-attacks/image/upload/v1676281581/docs/web/credentials/adding_autho.png)

> **Note:** The service you select will no longer
> be shown in since the connection has already been made.

With this connection with your provider
we will be able to access your organization and,
with this,
to all the repositories that you have there.
It will take into account the repositories that
have had activity in the last 60 days.
To see the list of these,
you can do it in the
[Outside](/machine/web/outside)
section.

![outside](https://res.cloudinary.com/fluid-attacks/image/upload/v1676282098/docs/web/credentials/out_of_scope.png)

> **Note:** The list of repositories that are listed
> in this view are repositories that are not associated
> with any group of that specific organization in the ARM.
> To see these,
> you must wait about 30 to 1 hour while the service connection is made.

## OAuth functionalities

### Remove oauth connection

You can remove the **OAuth credential** by
selecting the credential to be removed followed by the **Remove**
button.

![oauth remove](https://res.cloudinary.com/fluid-attacks/image/upload/v1676282499/docs/web/credentials/remove.png)

> **Note:** The credential will be removed along with
> its repositories listed in the
> [Outside](/machine/web/outside)
> section.
