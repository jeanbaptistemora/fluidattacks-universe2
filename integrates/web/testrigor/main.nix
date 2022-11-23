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
  replace = {
    __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.kubectl
      inputs.nixpkgs.python39
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/integrates/web/testrigor/runtime"
    ];
  };
  name = "integrates-web-testrigor";
  entrypoint = ./entrypoint.sh;
}
