# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeNodeJsEnvironment,
  projectPath,
  ...
}:
makeNodeJsEnvironment {
  name = "airs-npm";
  nodeJsVersion = "16";
  packageJson = projectPath "/airs/front/package.json";
  packageLockJson = projectPath "/airs/front/package-lock.json";
  shouldIgnoreScripts = true;
}
