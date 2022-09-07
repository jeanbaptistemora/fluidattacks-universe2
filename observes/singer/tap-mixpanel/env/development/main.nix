# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-singer-tap-mixpanel-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-mixpanel-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."${inputs.observesIndex.tap.mixpanel.env.runtime}"
    ];
  };
}
