# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{makeNodeJsEnvironment, ...}:
makeNodeJsEnvironment {
  name = "integrates-back-tools-secure-spreadsheet";
  nodeJsVersion = "14";
  packageJson = ./npm/package.json;
  packageLockJson = ./npm/package-lock.json;
}
