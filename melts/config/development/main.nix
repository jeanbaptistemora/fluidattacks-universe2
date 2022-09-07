# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makePythonPypiEnvironment,
  makeTemplate,
  inputs,
  ...
}: let
  pythonRequirements = makePythonPypiEnvironment {
    name = "melts-development";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
  makeTemplate {
    name = "melts-config-development";
    searchPaths = {
      bin = [inputs.nixpkgs.docker];
      source = [pythonRequirements];
    };
  }
