# Contributing

## Development environments

We want to be able to launch:
- Bash Shell / Terminal
- Code editor

And start developing X product with:
- Code auto-completion
- Go-to-definition functionality
- Required dependencies in the host
- etc

### Concepts

The ~/.bashrc file is a script that is loaded everytime you open a shell.
Functions, variables, and commands we place on the ~/.bashrc will help us configuring the shell environment automatically. The commands that we open in the shell after the bashrc is loaded (for example the code editor) will inherit such shell configurations.

### Nix

The tool that powers it all, install it as explained in
[Nix's download page](https://nixos.org/download.html):

### Tools

- Code editor:

  We highly recommend you use visual-studio-code because most of the team uses it
  and works very well for our purpose

- Other tools:

  Awscli, kubectl, vim, python, nodejs, git, ghc, jq, etc
