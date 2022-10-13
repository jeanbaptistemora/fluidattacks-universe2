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
  replace = {
    __argCertsDevelopment__ = outputs."/integrates/certs/dev";
    __argRuntime__ = outputs."/integrates/front/config/dev-runtime";
  };
  entrypoint = ./entrypoint.sh;
  name = "integrates-front";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-16_x
    ];
    source = [outputs."/integrates/front/config/dev-runtime-env"];
  };
}
