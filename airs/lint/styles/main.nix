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
    envAirsFront = projectPath "/airs/front";
    envAirsNpm = outputs."/airs/npm";
  };
  builder = ./builder.sh;
  name = "airs-lint-styles";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
    ];
    source = [outputs."/airs/npm/env"];
  };
}
