---
id: out-of-the-scope
title: Out of the scope
sidebar_label: Out of the scope
slug: /machine/web/out-of-the-scope
---

This section refers to repositories
not yet associated with any group
in the
[ARM platform](/machine/web/arm) of this organization.

This list of roots displayed is based on
the four providers that the ARM supports, which are:

- **GitLab:** List the groups/projects that the user has access to.
- **GitHub:** List the organizations/repositories the user has access to.
- **Bitbucket:** List the workspaces/projects/repositories
  that the user has access to.
- **Azure:** List the organizations/repositories the user has access to.

To see how to connect to these providers,
we invite you to enter the
[Global Credentials](/machine/web/machine/web/global-credentials)
section,
going to the Add repositories via OAuth section.

![OAuth view](https://res.cloudinary.com/fluid-attacks/image/upload/v1676300113/docs/web/azure/Four_providers.png)

When you see that you have
listed the credentials,
you go to the Out of Scope view,
and there you can see all the
repositories that are not yet
associated with the ARM and
that you have access with the
token given by adding an
[Azure DevOps PAT](/machine/web/groups/scope/roots/#adding-a-root-with-the-azure-devops-pat)
credential where you have access
to read source code.

![azure credentials view](https://res.cloudinary.com/fluid-attacks/image/upload/v1671713003/docs/web/azure/out_of_scope_view.png)

To add the repositories click
on the **plus symbol** in the action column.

![plus action](https://res.cloudinary.com/fluid-attacks/image/upload/v1671713134/docs/web/azure/pluss_action.png)

When you click on it,
you can specify to which
group of that organization
you will add that repository.

![justification](https://res.cloudinary.com/fluid-attacks/image/upload/v1671713422/docs/web/azure/justification.png)

When you click on the Confirm button,
you can start adding a new root,
as seen in the scope view,
having already set the URL of the
repository I had already chosen.

![add](https://res.cloudinary.com/fluid-attacks/image/upload/v1671713552/docs/web/azure/add.png)

In this way,
I select and add an Azure repository
to be analyzed.
