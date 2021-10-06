---
id: editor
title: Editor
sidebar_label: Editor
slug: /development/setup/editor
---

We highly recommend you use Visual Studio Code
because most of the team uses it
and works very well for our purpose.

You can install it with:
`$ NIXPKGS_ALLOW_UNFREE=1 nix-env -i vscode`

Now install some useful extensions:

```bash
extensions=(
  bbenoist.nix
  CoenraadS.bracket-pair-colorizer
  coolbear.systemd-unit-file
  eamodio.gitlens
  hashicorp.terraform
  haskell.haskell
  jkillian.custom-local-formatters
  justusadam.language-haskell
  mads-hartmann.bash-ide-vscode
  ms-python.python
  ms-python.vscode-pylance
  ms-toolsai.jupyter
  ms-toolsai.jupyter-keymap
  shardulm94.trailing-spaces
  streetsidesoftware.code-spell-checker
  tamasfe.even-better-toml
)
for extension in "${extensions[@]}"; do
  code --force --install-extension "${extension}"
done
```

For further customization a configuration file will be created at
`~/.config/Code/User/settings.json` once you start the editor.
Please note that
the entire configuration file
must comply the JSON format,
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

These configurations are suggested, you can add the ones you want:

```json
{
  "editor.rulers": [ 80 ],
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
      "command": "nixpkgs-fmt",
      "languages": [ "nix" ]
    },
    {
      "command": "/path/to/my/python/formatter/script",
      "languages": [ "python" ]
    },
    {
      "command": "shfmt -bn -ci -i 2 -s -sr -",
      "languages": [ "shellscript" ]
    },
    {
      "command": "terraform fmt",
      "languages": [ "tf" ]
    }
  ]
}
```

The Python formatter script can be this one:

```bash
#! /usr/bin/env /bash

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
