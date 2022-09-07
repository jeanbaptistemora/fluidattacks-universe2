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
  name = "skims-test-cli";
  replace = {
    __argSecretsFile__ = projectPath "/skims/secrets/dev.yaml";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.gnugrep
      outputs."/skims"
      inputs.nixpkgs.kubectl
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
