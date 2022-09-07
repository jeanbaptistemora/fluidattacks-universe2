# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeNodeJsModules,
  projectPath,
  ...
}:
makeNodeJsModules {
  name = "integrates-front-dev-runtime";
  nodeJsVersion = "14";
  packageJson = projectPath "/integrates/front/package.json";
  packageLockJson = projectPath "/integrates/front/package-lock.json";
}
