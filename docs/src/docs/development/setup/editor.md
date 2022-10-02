---
id: editor
title: Editor
sidebar_label: Editor
slug: /development/setup/editor
---

We highly recommend you use Visual Studio Code
because most of the team uses it,
and it works very well for our purpose.

You can install it with:

```bash
$ NIXPKGS_ALLOW_UNFREE=1 nix-env --install --attr vscode --file https://github.com/nixos/nixpkgs/archive/b42e50fe36242b1b205a7d501b7911d698218086.tar.gz
```

Now, from within a terminal
that was setup as explained in the previous tutorial,
open the [VS Code workspace][workspace]:

```bash
universe $ code universe.code-workspace
```

You will probably see a popup
to install the recommended extensions,
please install them:

![](https://res.cloudinary.com/fluid-attacks/image/upload/v1664733557/docs/development/setup/recommended-popup.png)

If you didn't see the popup,
please go to the extensions tab (`Ctrl+Shift+X`),
type `@recommended`,
and install the recommended extensions for the workspace.
You can click on the small cloud button
to the right of "WORKSPACE RECOMMENDATIONS"
and to the left of the pencil
to download them all at the same time:

![](https://res.cloudinary.com/fluid-attacks/image/upload/v1664733557/docs/development/setup/recommended-extensions.png)

You can test if everything works correctly by opening a JSON file,
adding empty lines between elements,
and then saving the file.
The empty lines should be removed,
and the keys sorted alphabetically.
In other words, the file should be automatically formatted on save.

For further customization,
you can add install other extensions
or open the settings with `Ctrl+,`
to configure things like the font, font size, or theme.
If you think an extension or setting can be useful
to other developers,
please add it to the [workspace][workspace] configuration.

Finally, take into account that certain extensions
or settings can prevent the environment from working.
Feel free to ask for help
in the _Development_ space on Google Workspace
if something doesn't work.

<!--  -->

[workspace]: https://gitlab.com/fluidattacks/universe/-/blob/trunk/universe.code-workspace
