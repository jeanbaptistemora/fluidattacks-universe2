# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-common-paginator-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-common-paginator-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/paginator/env/runtime"
    ];
  };
}
