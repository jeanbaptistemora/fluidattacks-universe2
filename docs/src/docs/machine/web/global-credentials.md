---
id: global-credentials
title: Global credentials
sidebar_label: Global credentials
slug: machine/web/global-credentials
---

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
  or [Azure DevOps PTA](/machine/web/groups/scope/roots#adding-a-root-with-the-azure-devops-pta)
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
