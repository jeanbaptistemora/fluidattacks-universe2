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
  searchPaths.bin = [outputs."${inputs.observesIndex.tap.announcekit.bin}"];
  name = "observes-singer-tap-announcekit-job-update-schema";
  entrypoint = ./entrypoint.sh;
}
