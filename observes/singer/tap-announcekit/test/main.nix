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
  name = "observes-singer-tap-announcekit-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.announcekit.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.announcekit.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}
