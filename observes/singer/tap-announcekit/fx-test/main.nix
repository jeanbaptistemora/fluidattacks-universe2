# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argEnvSrc__ = projectPath inputs.observesIndex.tap.announcekit.root;
    __argEnvTestDir__ = "fx_tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.announcekit.env.dev}"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-singer-tap-announcekit-fx-test";
  entrypoint = ./entrypoint.sh;
}
