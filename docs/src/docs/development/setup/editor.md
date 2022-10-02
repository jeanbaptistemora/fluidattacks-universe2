---
id: editor
title: Editor
sidebar_label: Editor
slug: /development/setup/editor
---

We highly recommend you use Visual Studio Code
because most of the team uses it,
and it works very well for our purpose.

You can install it with
`$ NIXPKGS_ALLOW_UNFREE=1 nix-env -i vscode`

Now, from within a terminal
that was setup as explained in the previous tutorial,
open the [VS Code workspace](https://gitlab.com/fluidattacks/universe/-/blob/trunk/universe.code-workspace):

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

For further customization,
a configuration file will be created at
`~/.config/Code/User/settings.json`
once you start the editor.
Please note that
the entire configuration file
must comply with the JSON format,
so make sure you don't have trailing commas.
If correctly formatted,
you should be able
to perform a `cat ~/.config/Code/User/settings.json | jq`
without errors.

This configuration is needed for the language server to work correctly:

```json
{
  "python.languageServer": "Pylance"
}
```

These configurations are suggested; you can add the ones you want:

```json
{
  "editor.rulers": [80],
  "files.insertFinalNewline": true,
  "files.trimFinalNewlines": true,
  "files.trimTrailingWhitespace": true
}
```

You can configure automatic code formatters like this:

```json
{
  "customLocalFormatters.formatters": [
    {
      "command": "/path/to/my/python/formatter/script",
      "languages": ["python"]
    },
    {
      "command": "shfmt -bn -ci -i 2 -s -sr -",
      "languages": ["shellscript"]
    },
    {
      "command": "terraform fmt",
      "languages": ["tf"]
    }
  ]
}
```

The Python formatter script can be this one:

```bash
#! /usr/bin/env bash

# Replace ${makesSrc} with the git-clone of:
# https://github.com/fluidattacks/makes

black \
  --config \
  "${makesSrc}/src/evaluator/modules/format-python/settings-black.toml" \
  - \
  | \
isort \
  --settings-path \
  "${makesSrc}/src/evaluator/modules/format-python/settings-isort.toml" \
  -
```
