# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  outputs,
  makeScript,
  inputs,
  ...
}:
makeScript {
  name = "integrates-execute-machine";
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
    ];
    source = [
      outputs."/melts/config/runtime"
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
