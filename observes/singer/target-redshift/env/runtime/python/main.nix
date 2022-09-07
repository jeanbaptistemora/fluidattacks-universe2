# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makePythonPypiEnvironment,
  inputs,
  ...
}:
makePythonPypiEnvironment {
  name = "observes-singer-target-redshift-env-runtime-python";
  searchPathsRuntime.bin = [
    inputs.nixpkgs.gcc
    inputs.nixpkgs.postgresql
  ];
  searchPathsBuild.bin = [
    inputs.nixpkgs.gcc
    inputs.nixpkgs.postgresql
  ];
  sourcesYaml = ./pypi-sources.yaml;
}
