---
id: gitroots
title: Git Roots
sidebar_label: Git Roots
slug: /machine/web/groups/scope/gitroots
---

In this section of the Scope tab, you can add and edit the repositories and environments
that we should take into account when performing penetration tests. In order to do this,
you can click on one of the three buttons that allow you to do different things.

### Add a git root

![Git Root Buttons](/img/web/groups/scope/git_root_buttons.png)

By clicking on the "Add git root" button the following form will show up

![Add New Root](/img/web/groups/scope/add_new_root.png)

In here you can specify the URL of your repository, the specific branch that we
will use to perform the penetration test and the kind of environment that it points to.

You can also choose if you would like a Health Check for the existing code, which means
that we would also review all the code already in the repository at the moment the
project starts, for an additional cost.

Lastly, you can specify parts of the repository that you would like us to ignore
while performing the penetration test. You can do this by clicking on the **plus(+)**
sign and a **pattern** for such files and/or folders. You can also click on the
**interrogation sign(?)** besides the word **gitignore** to access a web page that instructs
you on how to write the pattern used here.

After you complete the required fields, you can click on **Proceed** to add the Git Root,
or you can click on **Cancel** to discard all the information.

### Edit a git root

In order for the next button, **Edit root**, to become available you must first click on
one of the git roots you already added and the same form will show up again, albeit
slightly different

![Edit Root](/img/web/groups/scope/edit_root.png)

The form will have all the information of the Git Root you selected for you to modify.
You can change its environment kind, activate or deactivate the Health Check option,
add more gitignores or delete them by clicking on the trash icon to the right of the
specific gitignore you would like to delete.

Again, you can click on **Proceed** to apply the changes or on **Cancel** to discard them.

You might also wonder how to delete a git root, however this isn't possible in the ASM because
in the security world it is always better to keep records of everything. What you can do
is change a repository state to **Active** or **Inactive**, which would mean the following:

- **Active:** The repository is available and ready for our analysts to access.
- **Inactive:** The repository does not exist anymore, it was changed, or it was added by mistake.

Every time a repository is changed, a notification will be sent to all the people involved in the
project (both Fluid Attacks’s and the customer’s users). Finally, the states can be changed by
project users at any moment, and every change will be stored for future needs.

### Manage a git root environment

And lastly, after selecting one of your added **Git Roots**, you can also click on the
**Manage environments** button for the following form to show up

![Manage environments](/img/web/groups/scope/manage_envs.png)

You can click on the **plus(+)** button to add the environment URLs corresponding to the
selected Git Root, and also delete them by clicking on the trash button to the right
of the URL field. To discard or apply the changes you can click on **Cancel** or **Proceed**
respectively.
