# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeNodeJsModules,
  projectPath,
  ...
}:
makeNodeJsModules {
  name = "docs-runtime";
  nodeJsVersion = "16";
  packageJson = projectPath "/docs/src/package.json";
  packageLockJson = projectPath "/docs/src/package-lock.json";
}
