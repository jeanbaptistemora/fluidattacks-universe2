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
  name = "integrates-web-check-forces-output";
  replace = {
    __argIntegratesSecrets__ = projectPath "/integrates";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.kubectl
      outputs."/forces"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
