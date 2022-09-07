# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  inputs,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
      outputs."/forces"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
      outputs."/common/utils/sops"
      outputs."/melts/lib"
    ];
  };
  name = "forces-process-groups-break";
  entrypoint = ./entrypoint.sh;
}
