---
id: licencing-and-copyright
title: Licencing and Copyright
sidebar_label: Licencing and Copyright
slug: /development/licencing-and-copyright
---

We as a company, following the
Open Source philosophy,
are compromised to comply
with common Open Source standards.
One of those standards is the
[SPDX](https://spdx.dev/) which
improves our license and copyright
compliance.

We enforce this by making
our contributors to sign every
new file with the corresponding headers.

## License and Copyright Headers

To be compliant with the [SPDX](https://spdx.dev/)
standards we use a header commented on each file.

This is a License and Copyright header example:

```python
  # SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
  #
  # SPDX-License-Identifier: MPL-2.0
```

The contributor must sign each new file
added to the source code
so the change can be approved.

## Signing files

Software needed: [Reuse Helper Tool](https://git.fsfe.org/reuse/tool).
This tool can be installed with the next command
`nix-env -iA nixpkgs.reuse`.

We use [Reuse](https://reuse.software/) helper tool
to `lint` the source code checking the signature
and copyright presence for each file,
this is made on every developer/contributor
pipeline.

This also can be made individually by
running the next command:

```bash
  reuse lint
```

If everything is correct you will get the
next output:

```bash
  # SUMMARY

  * Bad licenses:
  * Deprecated licenses:
  * Licenses without file extension:
  * Missing licenses:
  * Unused licenses:
  * Used licenses: MPL-2.0
  * Read errors: 0
  * Files with copyright information: 7599 / 7599
  * Files with license information: 7599 / 7599

  Congratulations! Your project is compliant with version 3.0 of the REUSE Specification :-)
```

If you missed at least one signature
this tool will fail, showing this kind of output:

```bash
  # MISSING COPYRIGHT AND LICENSING INFORMATION

  The following files have no copyright and licensing information:
  * example.sh


  # SUMMARY

  * Bad licenses:
  * Deprecated licenses:
  * Licenses without file extension:
  * Missing licenses:
  * Unused licenses:
  * Used licenses: MPL-2.0
  * Read errors: 0
  * Files with copyright information: 7599 / 7600
  * Files with license information: 7599 / 7600

  Unfortunately, your project is not compliant with version 3.0 of the REUSE Specification :-(
```

In that case you can sign your file/s using this
command:

```bash
  reuse  addheader --copyright="Fluid Attacks <development@fluidattacks.com>" --license="MPL-2.0" --copyright-style spdx $filePath
```

Where `$filepath` is the relative path of the new file.

More info on how to add signatures using
the Reuse Helper Tool can be found [here](https://git.fsfe.org/reuse/tool#usage)
