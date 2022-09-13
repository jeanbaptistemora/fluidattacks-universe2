# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makePythonPypiEnvironment,
  ...
}:
makePythonPypiEnvironment rec {
  name = "skims-runtime";
  searchPathsBuild = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.gcc
    ];
    pythonPackage38 = [
      inputs.nixpkgs.python38Packages.pygraphviz
    ];
  };
  searchPathsRuntime = searchPathsBuild;
  sourcesYaml = ./sources.yaml;
  withSetuptools_57_4_0 = true;
  withWheel_0_37_0 = true;
}
