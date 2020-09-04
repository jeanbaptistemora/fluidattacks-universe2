# Contributing

## Python environment setup

0. Install `python3.8` in your operative system (use apt, dnf, etc)
0. Make sure your `PATH` environment variable contains the result of:

   `echo "$(python3.8 -m site --user-base)/bin"`

   In my case I added:

   `export PATH="${PATH}:/home/kamado/.local/bin"` to my direnv file.

   You can use your `~/.bashrc` too.

## Skims local environment setup

0. Enter the skims directory
0. Run:

   `./build.sh skims_install`

   This will build some things that need to exist for Skims to work.
   Run it every time you modify the `pyproject.toml` file.
0. Export your `INTEGRATES_API_TOKEN` as environment variable and ask for
   access to the test groups.

Optional yet useful steps:

0. Execute: `python3.8 -m pip install --user poetry`
0. Now you should be able to execute the development version of skims with:

   `poetry run skims --help`

   Every time you run Skims this way it'll reload modules.

   Changes made to the source-code are reflected immediately hence helping
   you to test changes.
0. There are some example config files inside the test folder that you can
   use to get started.
