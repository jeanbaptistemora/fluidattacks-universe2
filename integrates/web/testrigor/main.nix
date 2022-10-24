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
    __argTests__ = projectPath "/integrates/web/testrigor/tests";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.gawk
      inputs.nixpkgs.jq
    ];
    source = [
      outputs."/common/utils/sops"
    ];
  };
  name = "integrates-web-testrigor";
  entrypoint = ./entrypoint.sh;
}
