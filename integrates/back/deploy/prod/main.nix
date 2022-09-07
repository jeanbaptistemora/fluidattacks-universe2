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
    __argManifests__ = projectPath "/integrates/back/deploy/prod/k8s";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.curl
      inputs.nixpkgs.envsubst
      inputs.nixpkgs.kubectl
      inputs.nixpkgs.utillinux
      inputs.nixpkgs.yq
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  name = "integrates-back-deploy-prod";
  entrypoint = ./entrypoint.sh;
}
