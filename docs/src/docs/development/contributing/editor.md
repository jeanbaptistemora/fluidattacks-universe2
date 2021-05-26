---
id: editor
title: Editor
sidebar_label: Editor
slug: /development/stack/contributing/editor
---

We highly recommend you use Visual Studio Code because most of the team use it and works very well for our purpose

You can install it with:
`$ NIXPKGS_ALLOW_UNFREE=1 nix-env -i vscode-with-extensions -f /path/to/fluidattacks/product/repo`

The configuration file will be created at

`~/.config/Code/User/settings.json` once you start the editor

This configuration is needed for the language server to work correctly:

```json
{
    "python.languageServer": "Pylance",
}
```

These configurations are suggested, you can add the ones you want:

```json
{
    "editor.rulers": [ 80 ],
    "files.insertFinalNewline": true,
    "files.trimFinalNewlines": true,
    "files.trimTrailingWhitespace": true,
}
```

This configuration allows you to verify the code in real time and give the code the standard format:

```json
{
    "python.linting.prospectorEnabled": true,
    "python.linting.prospectorArgs": [
        "--profile",
        "<product_path>/makes/utils/lint-python/settings-prospector.yaml",
    ],
    "python.linting.mypyEnabled": true,
    "python.linting.mypyArgs": [
        "--config-file",
        "<product_path>/makes/utils/lint-python/settings-mypy.cfg"
    ],
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": [
        "--config",
        "<product_path>/makes/utils/python-format/settings-black.toml",
    ],
}
```
