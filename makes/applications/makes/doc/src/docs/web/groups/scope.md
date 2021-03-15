---
id: scope
title: Scope
sidebar_label: Scope
slug: /web/groups/scope
---

This section found in the last tab of your group's dashboard is where you will be able
to manage the [ToE](/web/glossary/#toe "Target of Evaluation").

## Git Roots

In this section of the Scope tab, you can add and edit the repositories and environments
that we should take into account when performing penetration tests. In order to do this,
you can click on one of the three buttons that allow you to do different things.

![Git Root Buttons](/img/git_root_buttons.png)

By clicking on the "Add git root" button the following form will show up

![Add New Root](/img/add_new_root.png)

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

In order for the next button, **Edit root**, to become available you must first click on
one of the git roots you already added and the same form will show up again, albeit
slightly different

![Edit Root](/img/edit_root.png)

The form will have all the information of the Git Root you selected for you to modify.
You can change its environment kind, activate or deactivate the Health Check option,
add more gitignores or delete them by clicking on the trash icon to the right of the
specific gitignore you would like to delete.

Again, you can click on **Proceed** to apply the changes or on **Cancel** to discard them.

And lastly, after selecting one of your added **Git Roots**, you can also click on the
**Manage environments** button for the following form to show up

![Manage environments](/img/manage_envs.png)

You can click on the **plus(+)** button to add the environment URLs corresponding to the
selected Git Root, and also delete them by clicking on the trash button to the right
of the URL field. To discard or apply the changes you can click on **Cancel** or **Proceed**
respectively.

## Files

In the Files section found in the Scope tab that you can see in the following image,
you can upload and download any files that you find useful or necessary for performing
penetration tests on the group.

![File Section](/img/file_section.png)

You can add them by clicking on the **Add** button and then the following window
will show up

![Add File](/img/add_file_modal.png)

Here you can look for the file that you want to upload, which cannot exceed a size
of 100 MB, and also add a meaningful description for the usage or purpose of the
added file. After this you can click on the **Proceed** button to upload the file
or the **Cancel** button to dismiss it.

When you have uploaded a file successfully it will be added to the table and if you
want to download it, you can click on it for the following window to show up

![File Options](/img/file_options_modal.png)

This way you can easily download or delete the file that you selected.

## Portfolio

In this section you will be able to add **Tags** to your groups to create portfolios.
In order to create a tag, you can click on the **Add** button.

![Portfolio Section](/img/portfolio_section.png)

When you click on it, a window will show up where you can add as many tags as you
want.

![Add Tag](/img/add_tags_modal.png)

To add a tag you can click on the **plus(+)** button below, when you click it,
more fields to add tags will appear, you can do this many times if you want to
add multiple tags. You can also click on the trash button in front of a tag
field to delete it if you decide to add less tags. When you have added the tag
or tags you want, click on **Proceed** to create them or you can click on
**Cancel** to dismiss them.

There is also the **Remove** button in the **Tags** section that is used to delete
any tags that you already created.

![Selected Tag](/img/selected_tag.png)

In order to enable this button, you need to click on one of the tags in the list.
After selecting it you can click on the remove button and the tag will be
inmediately deleted, so be careful when doing this.
