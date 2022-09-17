# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  name = "integrates-back-charts";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "integrates-back-charts-pypi";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
    pythonPackage = [
      (projectPath "/integrates/charts")
    ];
  };
}
