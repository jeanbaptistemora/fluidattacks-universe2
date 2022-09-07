# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.tap.git.root;
in
  makeTemplate {
    name = "observes-singer-tap-git-env-runtime";
    searchPaths = {
      pythonMypy = [
        self
      ];
      bin = [
        inputs.nixpkgs.git
      ];
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-singer-tap-git-env-runtime";
          sourcesYaml = ./pypi-sources.yaml;
        })
      ];
    };
  }
