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
  name = "skims-benchmark-owasp";
  replace = {
    __argBenchmarkRepo__ = inputs.skimsBenchmarkOwaspRepo;
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.python38
      outputs."/skims"
    ];
    source = [outputs."/skims/config/runtime"];
  };
  entrypoint = ./entrypoint.sh;
}
