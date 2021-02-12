
## Quick Start

Requirements:

1.  You'll need Nix,
    it can be installed as explained in the [tutorial](https://nixos.org/download.html).

Installing:

1.  Run the following command:

    `bash <(curl -L "https://fluidattacks.com/install/skims")`

1.  You should be able to execute skims now:

    `skims --help`

In order to run Skims you'll need a configuration file.

Let's assume that our target is a code repository located at `/path/to/MyAwesomeRepo`

```yaml
# Language that will be used, valid values are: EN, ES
language: EN

# You can use any string on this field, normally the name of the repository
namespace: MyAwesomeRepo

# Path to the repository
working_dir: /path/to/MyAwesomeRepo

# Target paths to test, relative to `working_dir`
path:
  include:
    # This includes a single folder
    - folder/

    # This includes a single file
    - file.extension

    # You can use UNIX style globs to match all files and directories
    - glob(*)

    # This is a recursive glob to match all typescript files
    - glob(**/*.ts)

    # Match all files and directories that contain 'abc' under src/java/
    - glob(src/java/*abc*)

    # This is a recursive glob to match all java files under src/java/
    - glob(src/java/**/*.java)
  exclude:
    # Exclude the test folder
    - test/
```

Running Skims:

```bash
$ skims /path/to/configuration/file
```
