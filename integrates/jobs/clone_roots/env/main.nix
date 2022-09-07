# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makePythonPypiEnvironment,
  inputs,
  ...
}:
makePythonPypiEnvironment {
  name = "clone-roots";
  searchPathsRuntime = {
    bin = [
      inputs.nixpkgs.git
      inputs.nixpkgs.openssh
    ];
  };
  sourcesYaml = ./pypi-sources.yaml;
}
