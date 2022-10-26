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
    __argSetupIntegratesFrontDevRuntime__ =
      outputs."/integrates/front/config/dev-runtime";
  };
  entrypoint = ./entrypoint.sh;
  name = "integrates-front-lint-stylelint";
  searchPaths = {
    bin = [inputs.nixpkgs.nodejs-18_x];
    source = [outputs."/integrates/front/config/dev-runtime-env"];
  };
}
