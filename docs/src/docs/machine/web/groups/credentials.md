---
id: global-credentials
title: Global credentials
sidebar_label: Credentials
slug: /machine/web/groups/global-credentials
---

You can store credentials in your
profile to use them across all
the groups in your organization.
To see the credentials you
have previously created,
you need to open the
[User information drop-down menu](/machine/web/user-information)
and click on **Credentials**.

![Menu Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1657298600/docs/web/groups/credentials/menu_credentials.png)

A pop-up window will appear,
where you can add,
edit or remove credentials.

![Window](https://res.cloudinary.com/fluid-attacks/image/upload/v1657298600/docs/web/groups/credentials/pop_up_window.png)

If you click on the Add button,
the following pop-up window will appear.
There,
you will need to enter a unique
name for the credential,
select the organization where it
will be available to all groups,
select the credential type (HTTPS or SSH)
and enter the credential information.

![Credentials Information](https://res.cloudinary.com/fluid-attacks/image/upload/v1657298600/docs/web/groups/credentials/credentials_infor.png)

After you successfully
add your new credential,
it will show up in the table.
From then on,
it will appear as an
[existing credential](/machine/web/groups/scope/roots#existing-credentials)
when adding or editing a Git root.

![Existing Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1657298600/docs/web/groups/credentials/existing_credential.png)

If you click on the edit icon
in the Action column,
a pop-up window will appear.
There,
you can change the name of
the credential and,
if you toggle on the
**New secrets** option,
change the credential information.

![New Secrets](https://res.cloudinary.com/fluid-attacks/image/upload/v1657298600/docs/web/groups/credentials/new_secrets.png)

If you click on the remove
icon in the Action column,
a warning window will appear
asking for your confirmation.

![Remove Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1657298601/docs/web/groups/credentials/remove_credentials.png)

The following are some points to
keep in mind regarding credentials:

- If the credential is removed,
  it is also removed from all
  the git roots that were using it.
- When a stakeholder is removed
  from the organization,
  then their credentials are
  removed from that organization.
- If the credential is added in a
  Git root then that credential can
  only be managed by that stakeholder.
- For a stakeholder to be able
  to use your credentials,
  the latter have to be already
  in use by any Git root in a
  group the former has access to,
  and the stakeholder needs to
  have permissions for editing roots.
