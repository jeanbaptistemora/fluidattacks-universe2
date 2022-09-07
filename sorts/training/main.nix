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
  name = "sorts-training";
  searchPaths = {
    bin = [inputs.nixpkgs.python38];
    source = [
      outputs."/sorts/config/development"
      outputs."/sorts/config/runtime"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
