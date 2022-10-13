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
    envSetupIntegratesFrontDevRuntime =
      outputs."/integrates/front/config/dev-runtime";
    envSrcIntegratesFront = projectPath "/integrates/front";
  };
  builder = ./builder.sh;
  name = "integrates-front-test";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-16_x
    ];
    source = [outputs."/integrates/front/config/dev-runtime-env"];
  };
}
