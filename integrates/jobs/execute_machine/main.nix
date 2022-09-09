# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  outputs,
  makeScript,
  inputs,
  makePythonVersion,
  ...
}:
makeScript {
  name = "integrates-execute-machine";
  replace = {
    __argScript__ = ./src/__init__.py;
  };
  searchPaths = {
    bin = [
      (makePythonVersion "3.9")
      inputs.nixpkgs.jq
      inputs.nixpkgs.findutils
    ];
    source = [
      outputs."/skims/config/runtime"
      outputs."/melts/config/runtime"
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
