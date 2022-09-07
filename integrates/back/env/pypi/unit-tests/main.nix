# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makePythonPypiEnvironment,
  inputs,
  ...
}:
makePythonPypiEnvironment {
  name = "integrates-back-unit-tests";
  searchPathsBuild = {
    bin = [inputs.nixpkgs.gcc];
  };
  searchPathsRuntime = {
    bin = [inputs.nixpkgs.gcc];
  };
  sourcesYaml = ./pypi-sources.yaml;
  withSetuptools_57_4_0 = true;
  withWheel_0_37_0 = true;
}
