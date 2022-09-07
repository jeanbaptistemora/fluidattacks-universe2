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
  name = "observes-singer-tap-csv-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.csv.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.csv.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}
