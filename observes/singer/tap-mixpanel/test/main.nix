# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  name = "observes-singer-tap-mixpanel-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.mixpanel.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.mixpanel.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}
