# Contributing

## Development environments

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

1. **Concepts**

    The `~/.bashrc` file is a script that is loaded everytime you open a Bash shell.
    Functions, variables, and commands we place on the `~/.bashrc` will help us to
    configure the environment automatically.
    The commands that we open in the shell after the `~/.bashrc` is loaded
    (or `$ source ~/.bashrc`-ed),
    for example the code editor, will inherit such shell configurations

1. **Nix**

    The tool that powers it all, install it as explained in
    [Nix's download page](https://nixos.org/download.html)

1. **Product dependencies**

    Below snippets should be added to the end of your `~/.bashrc`.
    We highly recommend you to only use one snippet at a time because
    different products can overlap with each other

    Everytime you modify the `~/.bashrc` you should execute `$ source ~/.bashrc`,
    otherwise changes won't be visible

    All the programs and tools that you open from within the Bash Shell will
    be able to see the configurations we made

    - **Integrates**

        - **Back**

            ```bash
            # Replace the following values with real ones
            export INTEGRATES_DEV_AWS_ACCESS_KEY_ID='test'
            export INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY='test'

                cd /path/to/fluidattacks/product/repo \
            &&  ./m makes.dev.integrates.back \
            &&  source out/makes-dev-integrates-back
            ```

    - **Observes**

        - **Tap Mixpanel**

            ```bash
                cd /path/to/fluidattacks/product/repo \
            &&  ./m makes.dev.observes.tap-mixpanel \
            &&  source out/makes-dev-observes-tap-mixpanel
            ```

    - **Skims**

        ```bash
            cd /path/to/fluidattacks/product/repo \
        &&  ./m makes.dev.skims \
        &&  source out/makes-dev-skims
        ```

1. **Other tools**

    - Code editor:

      We highly recommend you use Visual Studio Code because most of the team use it and works very well for our purpose

      You can install it with:
      `$ nix-env -i makes-dev-vscode -f /path/to/fluidattacks/product/repo`

    - Others:

      awscli, curl, kubectl, vim, python, nodejs, git, ghc, jq, etc

      You can install them with:
      `$ nix-env -i $tool_name`

      For example: `$ nix-env -i awscli`

1. **Openining the environment**

    At this point you can open a Bash Shell,
    execute `$ code`, and the code editor will be able to auto-complete,
    jump-to-definition, etc

    Additionally your Bash shell will be able to locate the dependencies of the product,
    in case you need to debug
