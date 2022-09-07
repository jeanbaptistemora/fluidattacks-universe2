# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  makePythonPypiEnvironment,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-singer-tap-mailchimp-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-mailchimp-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."${inputs.observesIndex.tap.mailchimp.env.runtime}"
    ];
  };
}
