# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.announcekit.bin}"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-singer-tap-announcekit-fx-test-stream";
  entrypoint = ./entrypoint.sh;
}
