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
  entrypoint = ./entrypoint.sh;
  name = "integrates-streams";
  replace = {
    __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
    __argSecretsProd__ = projectPath "/integrates/secrets/production.yaml";
    __argSrc__ = projectPath "/integrates/streams/src";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.python39
    ];
    source = [
      outputs."/common/utils/sops"
      outputs."/integrates/streams/runtime"
    ];
  };
}
