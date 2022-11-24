---
id: licensing-and-copyright
title: Licensing and Copyright
sidebar_label: Licensing and Copyright
slug: /development/licensing-and-copyright
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
standards we use a [DEP5](https://reuse.software/spec/#dep5) file
stored in `.reuse/dep5`.

All existing files in the repository must be specified in such file.

## Reviewing files

Software needed: [Makes](https://github.com/fluidattacks/makes).

We use an extension of the
[Reuse Helper Tool](https://git.fsfe.org/reuse/tool)
and Makes, which lints
files and makes sure
that all of them are compliant.

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
```

If you missed at least one file
the extension will fail and let you know
which files need to be specified
in the [DEP5 file](https://gitlab.com/fluidattacks/universe/-/blob/trunk/.reuse/dep5)

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
  [ERROR] Some files are not properly licensed. Please adapt the licensing file under ./reuse/dep5
```

More info on how to add signatures using
the Reuse Helper Tool can be found [here](https://git.fsfe.org/reuse/tool#usage)
