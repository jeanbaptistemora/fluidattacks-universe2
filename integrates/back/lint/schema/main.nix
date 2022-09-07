# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  libGit,
  makeScript,
  makeNodeJsEnvironment,
  ...
}: let
  name = "integrates-back-lint-schema";
  nodeJsEnvironment = makeNodeJsEnvironment {
    inherit name;
    nodeJsVersion = "14";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeScript {
    entrypoint = ./entrypoint.sh;
    inherit name;
    searchPaths = {
      bin = [
        inputs.nixpkgs.git
        inputs.nixpkgs.openssh
      ];
      source = [
        libGit
        nodeJsEnvironment
      ];
    };
  }
