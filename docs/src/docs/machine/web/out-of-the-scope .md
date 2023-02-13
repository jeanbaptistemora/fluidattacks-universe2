---
id: out-of-the-scope
title: Out of the scope
sidebar_label: Out of the scope
slug: /machine/web/out-of-the-scope
---

This section refers to repositories
that are not yet associated to any
group in the ARM platform.

To see if you have any Azure
type credentials,
you can check in the
[Global credentials](/machine/web/machine/web/global-credentials/)
view in the column named **Type**.

![azure in credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1671712645/docs/web/azure/out_of_scope.png)

If you don't know how to add
an Azure DevOps PAT credential,
you can do it in two parts:
[Scope](/machine/web/groups/scope/roots/#adding-a-root-with-the-azure-devops-pat)
or [Global credentials](/machine/web/machine/web/global-credentials/).

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
