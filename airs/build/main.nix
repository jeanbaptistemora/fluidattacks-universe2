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
    __argAirsNpm__ = outputs."/airs/npm";
    __argAirsSecrets__ = projectPath "/airs/secrets";
  };
  entrypoint = ./entrypoint.sh;
  name = "airs-build";
  searchPaths = {
    rpath = [
      inputs.nixpkgs.musl
    ];
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnugrep
      inputs.nixpkgs.gnused
      inputs.nixpkgs.nodejs-16_x
      inputs.nixpkgs.utillinux
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/airs/npm/runtime"
      outputs."/airs/npm/env"
      outputs."/common/utils/sops"
    ];
  };
}
