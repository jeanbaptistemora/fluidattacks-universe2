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
  name = "integrates-front-lint-eslint";
  searchPaths = {
    bin = [inputs.nixpkgs.nodejs-14_x];
    source = [
      outputs."/common/utils/lint-typescript"
      outputs."/integrates/front/config/dev-runtime-env"
    ];
  };
}
