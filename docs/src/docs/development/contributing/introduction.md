---
id: introduction
title: Introduction
sidebar_label: Introduction
slug: /development/stack/contributing/introduction
---

We want to be able to launch:
- Bash shell (Terminal)
- Code editor

And start developing X product with:
- Code auto-completion
- Go-to-definition functionality
- Required dependencies in the host
- etc

This tutorial works from top to bottom,
so read it completely and execute commands as you read

## Concepts

### Bashrc

The `~/.bashrc` file is a script that is loaded everytime you open a Bash shell.
Functions, variables, and commands we place on the `~/.bashrc` will help us to
configure the environment automatically.
The commands that we open in the shell after the `~/.bashrc` is loaded
(or `$ source ~/.bashrc`-ed),
for example the code editor, will inherit such shell configurations

### Nix

The tool that powers it all, install it as explained in
[Nix's download page](https://nixos.org/download.html)
