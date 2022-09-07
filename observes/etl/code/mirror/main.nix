# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  inputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      outputs."/melts"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
    ];
  };
  name = "observes-etl-code-mirror";
  entrypoint = ./entrypoint.sh;
}
