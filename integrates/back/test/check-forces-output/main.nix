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
  name = "check-forces-output";
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argIntegratesSecrets__ = projectPath "/integrates";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.coreutils
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
      outputs."/forces"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
