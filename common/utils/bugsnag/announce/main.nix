# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeNodeJsEnvironment,
  makeScript,
  ...
}: let
  nodeJsEnvironment = makeNodeJsEnvironment {
    name = "bugsnag-announce";
    nodeJsVersion = "14";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeScript {
    entrypoint = ./entrypoint.sh;
    name = "bugsnag-announce";
    searchPaths.source = [nodeJsEnvironment];
  }
