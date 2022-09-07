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
  name = "melts-test";
  searchPaths = {
    source = [
      outputs."/melts/config/development"
      outputs."/melts/config/runtime"
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
    ];
    bin = [
      inputs.nixpkgs.gnugrep
    ];
  };
  entrypoint = ./entrypoint.sh;
}
