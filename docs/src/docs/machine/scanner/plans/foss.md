---
id: foss
title: Free and Open Source
sidebar_label: Free and Open Source
slug: /machine/scanner/plans/foss
---

When run as as a free
and Open Source CLI tool,
you are in charge of
configuring the tool.
It will scan vulnerabilities
in the target of your choice
and report results back to you
in pretty-printed or CSV format:

- Pretty Printed results:

  ```markup
  [INFO] F052. Insecure encryption algorithm: OWASP/src/main/java/org/owasp/benchmark/testcode/BenchmarkTest00035.java

  ¦ line  ¦ Data                                                                                                                     ¦
  ¦ ----- ¦ ------------------------------------------------------------------------------------------------------------------------ ¦
  ¦    64 ¦ .getClass().getClassLoader().getResourceAsStream("benchmark.properties"));                                               ¦
  ¦    65 ¦ ithm = benchmarkprops.getProperty("cryptoAlg1", "DESede/ECB/PKCS5Padding");                                              ¦
  ¦    66 ¦ .Cipher c = javax.crypto.Cipher.getInstance(algorithm);                                                                  ¦
  ¦    67 ¦                                                                                                                          ¦
  ¦    68 ¦ he cipher to encrypt                                                                                                     ¦
  ¦  > 69 ¦ .SecretKey key = javax.crypto.KeyGenerator.getInstance("DES").generateKey();                                             ¦
  ¦    70 ¦ .crypto.Cipher.ENCRYPT_MODE, key);                                                                                       ¦
  ¦    71 ¦                                                                                                                          ¦
  ¦    72 ¦ nd store the results                                                                                                     ¦
  ¦    73 ¦  = {(byte) '?'};                                                                                                         ¦
  ¦    74 ¦ Param = param;                                                                                                           ¦
  ¦    75 ¦ am instanceof String) input = ((String) inputParam).getBytes();                                                          ¦
  ¦    76 ¦ am instanceof java.io.InputStream) {                                                                                     ¦
  ¦    77 ¦ trInput = new byte[1000];                                                                                                ¦
  ¦    78 ¦ ((java.io.InputStream) inputParam).read(strInput);                                                                       ¦
  ¦    79 ¦  -1) {                                                                                                                   ¦
  ¦    80 ¦ onse.getWriter()                                                                                                         ¦
  ¦    81 ¦     .println(                                                                                                            ¦
  ¦    82 ¦             "This input source requires a POST, not a GET. Incompatible UI for the InputStream source.");                ¦
  ¦    83 ¦ rn;                                                                                                                      ¦
  ¦    84 ¦                                                                                                                          ¦
  ¦ ----- ¦ ------------------------------------------------------------------------------------------------------------------------ ¦
          ^ Column 24
  ```

- CSV results:

| title | what | where | cwe |
|-------|------|-------|-----|
| F052. Insecure encryption algorithm | OWASP/src/main/java/org/owasp/benchmark/testcode/BenchmarkTest00035.java | 69 | 310 + 327 |

## Requirements

1. A x86_64-linux system:

    ```bash
    $ uname -mo
    x86_64 GNU/Linux
    ```

1. Bash v5, installed as explained in the
    [Bash's download page](https://www.gnu.org/software/bash/#download).

1. Curl v7, installed as explained in the
    [Curl's download page](https://curl.se/download.html).

1. Nix v2, installed as explained in the
    [Nix's download page](https://nixos.org/download).

1. Makes, installed like this:

    ```bash
    $ curl -L fluidattacks.com/install/m | sh
    ```

## Using

```bash
$ m gitlab:fluidattacks/product@master /skims --help

  Usage: skims [OPTIONS] COMMAND [ARGS]...

    Deterministic vulnerability life-cycle reporting and closing tool.

  ...
```

## Running the scanner

```bash
$ m gitlab:fluidattacks/product@master /skims scan /path/to/config.yaml

  ... 🚀 !!
```

### Configuration format

Fluid Attack's scanner
uses a configuration file in
[YAML](https://yaml.org/) syntax.

```yaml
# Description:
#   Pick a name you like, normally the name of the repository.
# Example:
namespace: repository

# Description:
#   Omit if you want pretty-printed results,
#   Set to a path if you want CSV results.
# Optional:
#   Yes
# Example:
output: /path/to/results.csv

# Description:
#   Working directory, normally used as the path to the repository.
# Example:
working_dir: /path/to/your/repository

# Description:
#   SAST for source code.
# Example:
path:
  # Description:
  #   Target files used in the analysis.
  # Example:
  include:
    # Absolute path
    - /path/to/file/or/dir
    # Relative path to `working_dir`
    - src/main/java/org/test/Test.java
    # Unix-style globs
    - glob(*)
    - glob(**.java)
    - glob(src/**/test*.py)

# Description:
#   DAST for HTTP.
http:
  # Description:
  #   Target HTTP urls used in the analysis.
  # Example:
  include:
    - http://example.com/

# Description:
#  Reversing checks for Android APKs.
apk:
  # Description:
  #   Target files used in the analysis.
  # Example:
  include:
    # Absolute path
    - /path/to/build/awesome-app-v1.0.apk
    # Relative path to `working_dir`
    - build/awesome-app-v1.0.apk

# Description:
#  DAST for SSL.
ssl:
  # Description:
  #   Target host and port used in the analysis.
  # Example:
  include:
    - host: example.com
      port: 443

# Description:
#   Findings to analyze.
#   The complete list of findings can be found here:
#   https://gitlab.com/fluidattacks/product/-/blob/master/skims/manifests/findings.lst
# Optional:
#   Yes, if not present all security findings will be analyzed.
# Example:
checks:
- F052

# Description:
#   Language to use, valid values are: EN, ES.
# Optional:
#   Yes, defaults to: EN.
language: EN
```
