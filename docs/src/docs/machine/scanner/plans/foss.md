---
id: foss
title: Free and Open Source
sidebar_label: Free and Open Source
slug: /machine/scanner/plans/foss
---

When run as as a free and Open Source CLI tool,
you are in charge of configuring the tool.
It will scan vulnerabilities in the target of your choice
and report results back to you in pretty-printed or CSV format:

- Pretty Printed results:

  ```
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

1.  A x86_64-linux system:

    ```bash
    $ uname -mo
    x86_64 GNU/Linux
    ```

1.  Bash v5, installed as explained in the
    [Bash's download page](https://www.gnu.org/software/bash/#download).

1.  Curl v7, installed as explained in the
    [Curl's download page](https://curl.se/download.html).

1.  Nix v2, installed as explained in the
    [Nix's download page](https://nixos.org/download).

## Installing

1.  Run the following command:

    `$ bash <(curl -L fluidattacks.com/install/skims)`

1.  You should be able to execute the scanner now:

    `$ skims --help`

## Running the scanner

Just execute `$ skims /path/to/config.yaml`.

### Configuration format
