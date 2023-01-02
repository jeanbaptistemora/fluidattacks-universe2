---
id: clients
title: For Clients
sidebar_label: For Clients
slug: /about/security/authorization/clients
---

Our [Attack Resistance Management (ARM)](https://app.fluidattacks.com/)
has a set of necessary
[roles](/criteria/requirements/096)
for every hacking project.

Once the client decides
which members of their team should be **project managers**,
`Fluid Attacks` assigns them the role,
providing them
the [ability to give](/criteria/requirements/035)
the [minimum required permissions](/criteria/requirements/186)
to other members of their team.

To protect the
information of each group,
which is the source code
and its vulnerabilities,
authorization is based on the
[Role-Based Access Control (RBAC)](https://auth0.com/docs/manage-users/access-control/rbac)
model,
which will give access to the data
through Roles and division of the
projects (Groups).

The people with the roles
(**User Manager & Customer Manager**)
can define which team members
will have access to the different
groups and roles.
These can be divided into three levels:

- Role at Organization level.
- Role at Group level.

Remember that all users using the
[Attack Resistance Management (ARM)](https://app.fluidattacks.com/)
can execute actions given
according to each role,
if you want to see the
actions we invite you to enter
[here](/machine/web/groups/roles/#roles-table).

## Requirements

- [035. Manage privilege modifications](/criteria/requirements/035)
- [095. Define users with privileges](/criteria/requirements/095)
- [096. Set user's required privileges](/criteria/requirements/096)
- [186. Use the principle of least privilege](/criteria/requirements/186)
