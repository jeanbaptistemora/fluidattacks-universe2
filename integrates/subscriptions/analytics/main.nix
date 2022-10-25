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
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-subscriptions-analytics";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python39
      outputs."/integrates/db"
      outputs."/integrates/storage"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
