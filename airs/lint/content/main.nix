# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  env = {
    envAirs = projectPath "/airs";
    envExclude = ./exclude.lst;
  };
  builder = ./builder.sh;
  name = "airs-lint-content";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnused
    ];
    source = [
      outputs."/airs/lint/md"
      outputs."/common/utils/common"
    ];
  };
}
