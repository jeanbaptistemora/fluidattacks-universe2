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

Software needed: [Makes](https://github.com/fluidattacks/makes).

We use an extension of the
[Reuse Helper Tool](https://git.fsfe.org/reuse/tool)
and Makes, which lints
and format files automatically with the corresponding header.

This extension can be executed with
the next command, while being at the root of
our repository:

```bash
  m . /common/utils/license
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
  [INFO] Nothing to format here! All files are licensed
```

If you missed at least one signature
the extension will fail and will
automatically format the specified files.
This is an example of the output:

```bash
  # MISSING COPYRIGHT AND LICENSING INFORMATION

  The following files have no licensing information:
  * common/utils/license/entrypoint.sh


  # SUMMARY

  * Bad licenses:
  * Deprecated licenses:
  * Licenses without file extension:
  * Missing licenses:
  * Unused licenses:
  * Used licenses: MPL-2.0
  * Read errors: 0
  * Files with copyright information: 7814 / 7814
  * Files with license information: 7813 / 7814

  Unfortunately, your project is not compliant with version 3.0 of the REUSE Specification :-(
  [INFO] Adding License and Copyright headers to files
  [INFO] Formatted files successfully!
```

More info on how to add signatures using
the Reuse Helper Tool can be found [here](https://git.fsfe.org/reuse/tool#usage)
