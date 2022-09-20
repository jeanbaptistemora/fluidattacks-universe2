# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.tap.timedoctor.root;
in
  makeTemplate {
    name = "observes-singer-tap-timedoctor-env-runtime";
    searchPaths = {
      bin = [
        inputs.nixpkgs.python38
      ];
      pythonPackage = [
        self
      ];
    };
  }
