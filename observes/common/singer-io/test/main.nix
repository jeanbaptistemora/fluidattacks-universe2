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
  name = "observes-common-singer-io-test";
  env = {
    envSrc = projectPath inputs.observesIndex.common.singer_io.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."/observes/common/singer-io/env/development"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}
