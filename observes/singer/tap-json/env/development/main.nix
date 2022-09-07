# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-singer-tap-json-env-development";
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.json.env.runtime}"
    ];
  };
}
