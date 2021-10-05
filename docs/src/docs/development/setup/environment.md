---
id: environment
title: Environment
sidebar_label: Environment
slug: /development/setup/environment
---

## Others tools

For tools like
`awscli`,
`curl`,
`kubectl`,
`vim`,
`python`,
`nodejs`,
`git`,
`ghc`,
`jq`,
etc.

You can run:
`$ nix-env -i $tool_name`.

This will install such tool.

For example: `$ nix-env -i awscli`

## Opening the environment

At this point you can open a Bash Shell,
execute `$ code`, and the code editor will be able to auto-complete,
jump-to-definition, etc

Additionally your Bash shell will be able to locate the dependencies of the product,
in case you need to debug
