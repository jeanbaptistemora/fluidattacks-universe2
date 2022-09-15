# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makePythonPypiEnvironment,
  inputs,
  ...
}:
makePythonPypiEnvironment {
  name = "integrates-streams-runtime";
  sourcesYaml = ./pypi-sources.yaml;
  searchPathsBuild = {
    bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
  };
  searchPathsRuntime = {
    bin = [
      inputs.nixpkgs.gcc
      inputs.nixpkgs.postgresql
    ];
  };
}
