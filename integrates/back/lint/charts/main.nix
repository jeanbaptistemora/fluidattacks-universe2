# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeDerivation,
  makeNodeJsEnvironment,
  projectPath,
  ...
}: let
  name = "integrates-back-lint-charts";
  nodeJsEnvironment = makeNodeJsEnvironment {
    inherit name;
    nodeJsVersion = "18";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeDerivation {
    builder = ./builder.sh;
    env.envSrc = projectPath "/integrates/back/src/app/templates/static/graphics";
    inherit name;
    searchPaths.source = [nodeJsEnvironment];
  }
