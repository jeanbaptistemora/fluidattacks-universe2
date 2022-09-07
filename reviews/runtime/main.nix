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
    __argSrcReviews__ = projectPath "/reviews/src";
  };
  name = "reviews-runtime";
  searchPaths = {
    bin = [inputs.nixpkgs.python310];
    pythonPackage = [(projectPath "/reviews/src")];
    source = [
      (makePythonPypiEnvironment {
        name = "reviews-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
  template = ./template.sh;
}
