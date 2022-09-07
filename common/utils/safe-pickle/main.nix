# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makePythonPypiEnvironment,
  makeTemplate,
  ...
}:
makeTemplate {
  name = "common-python-safe-pickle";
  searchPaths = {
    pythonPackage = [./src];
    source = [
      (makePythonPypiEnvironment {
        name = "common-python-safe-pickle";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
