# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argSrcForces__ = projectPath "/forces";
  };
  name = "forces-config-runtime";
  searchPaths = {
    bin = [
      inputs.nixpkgs.git
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "forces-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
    pythonPackage = [
      (projectPath "/common/utils/bugsnag/client")
      (projectPath "/forces")
    ];
  };
  template = ./template.sh;
}
