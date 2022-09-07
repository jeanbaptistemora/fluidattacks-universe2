# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeNodeJsEnvironment,
  makeScript,
  ...
}: let
  nodeJsEnvironment = makeNodeJsEnvironment {
    name = "bugsnag-source-map-uploader";
    nodeJsVersion = "14";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeScript {
    name = "bugsnag-source-map-uploader";
    searchPaths = {
      source = [nodeJsEnvironment];
    };
    entrypoint = ./entrypoint.sh;
  }
